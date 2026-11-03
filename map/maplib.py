"""Shared engine for Computation Quests maps built from the La Petite Tile Maps pack.

The pack is read from LaPetiteTile_Maps/ at the repo root (override with the
TILES env var). It is not committed to the repository; see map/README.md.

Ground tiles are pointy-top hexes: 16x16 images, rows 12px apart, odd rows
shifted right by half a tile.
"""
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PACK = os.environ.get('TILES', os.path.join(ROOT, 'LaPetiteTile_Maps'))
TEX = os.path.join(PACK, 'Textures')

T, DX, DY = 16, 16, 12
DEEP = (80, 98, 124, 255)
INK = (58, 38, 24, 255)
PALE = (238, 232, 214, 255)


# ---------------------------------------------------------------- utilities

def tex(*parts):
    return Image.open(os.path.join(TEX, *parts)).convert('RGBA')


def font(size=16, name='Chandelle'):
    return ImageFont.truetype(os.path.join(PACK, 'Fonts', name + '.ttf'), size)


def lum(p):
    return 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]


def brightness(tile):
    return lum(ImageStat.Stat(tile.convert('RGB'), mask=tile.getchannel('A')).mean)


class Noise:
    """Smooth 2D value noise."""

    def __init__(self, seed, cell):
        self.r = random.Random(seed)
        self.cell = cell
        self.g = {}

    def _v(self, i, j):
        if (i, j) not in self.g:
            self.g[(i, j)] = self.r.random()
        return self.g[(i, j)]

    def __call__(self, x, y):
        x, y = x / self.cell, y / self.cell
        i, j = math.floor(x), math.floor(y)
        fx, fy = x - i, y - j
        sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        a = self._v(i, j) + sx * (self._v(i + 1, j) - self._v(i, j))
        b = self._v(i, j + 1) + sx * (self._v(i + 1, j + 1) - self._v(i, j + 1))
        return a + sy * (b - a)


def blob_field(blobs, n1, n2):
    """Land value from ellipses (cx, cy, rx, ry[, roughness]); land where > 0."""
    def field(x, y):
        best, rough = -9, 1.0
        for b in blobs:
            v = 1 - math.hypot((x - b[0]) / b[2], (y - b[1]) / b[3])
            if v > best:
                best, rough = v, (b[4] if len(b) > 4 else 1.0)
        return best + ((n1(x, y) - 0.5) * 0.55 + (n2(x, y) - 0.5) * 0.25) * rough - 0.12
    return field


# ---------------------------------------------------------------- tiles

def ground_tiles(name):
    """Full-hex tiles from a ground tileset (skips edge and corner pieces)."""
    im = tex('Tileset_Ground', name + '.png')
    px = im.load()
    out = []
    for ty in range(im.height // T):
        for tx in range(im.width // T):
            X, Y = tx * T, ty * T
            pts = [(8, 0), (7, 15), (0, 8), (15, 8), (8, 8), (0, 4), (15, 11), (0, 11), (15, 4)]
            if not all(px[X + x, Y + y][3] for x, y in pts):
                continue
            ops = [px[X + x, Y + y] for x in range(T) for y in range(T) if px[X + x, Y + y][3]]
            base = sorted(lum(p) for p in ops)[len(ops) // 2]
            dark = sum(1 for x in range(T) for y in range(11, 16)
                       if px[X + x, Y + y][3] and lum(px[X + x, Y + y]) < base - 25)
            if dark < 2:
                out.append(im.crop((X, Y, X + T, Y + T)))
    return out


def decal_tiles(folder, name):
    """Every non-empty 16x16 tile from a sheet."""
    im = tex(folder, name + '.png')
    out = []
    for ty in range(im.height // T):
        for tx in range(im.width // T):
            t = im.crop((tx * T, ty * T, tx * T + T, ty * T + T))
            if t.getbbox():
                out.append(t)
    return out


class HexMap:
    def __init__(self, cols, rows, seed):
        self.cols, self.rows, self.seed = cols, rows, seed
        self.W, self.H = cols * DX + 8, rows * DY + 4
        self.rnd = random.Random(seed)

    def hexpos(self, c, r):
        return c * DX + (8 if r % 2 else 0), r * DY

    def center(self, c, r):
        x, y = self.hexpos(c, r)
        return x + 8, y + 8

    def nbrs(self, c, r):
        a = [(c - 1, r), (c + 1, r)]
        for rr in (r - 1, r + 1):
            a += [(c - 1, rr), (c, rr)] if r % 2 == 0 else [(c, rr), (c + 1, rr)]
        return [(x, y) for x, y in a if 0 <= x < self.cols and 0 <= y < self.rows]

    def grow(self, m):
        o = [row[:] for row in m]
        for r in range(self.rows):
            for c in range(self.cols):
                if m[r][c]:
                    for nc, nr in self.nbrs(c, r):
                        o[nr][nc] = True
        return o

    def cells(self):
        return ((c, r) for r in range(self.rows) for c in range(self.cols))

    def terrain(self, img, land_fn, zone_fn, beach_fn=None, decals=(), edge=28):
        """Paint water rings, beaches, ground and overlays. Returns the land mask.

        land_fn(x, y) -> float, land where > 0.
        zone_fn(x, y) -> 'grass' | 'snow' | 'sand' | 'rock'.
        beach_fn(x, y) -> bool, whether coast next to (x, y) gets a beach.
        decals: (tiles, cx, cy, rx, ry, chance) patches painted over land.
        edge: margin kept as open water; 0 lets land run off the map.
        """
        rnd = self.rnd
        land = [[False] * self.cols for _ in range(self.rows)]
        for c, r in self.cells():
            x, y = self.center(c, r)
            if edge < x < self.W - edge and edge < y < self.H - edge:
                land[r][c] = land_fn(x, y) > 0

        ocean = sorted(ground_tiles('Tileset_Ground_Ocean'), key=lambda t: -brightness(t))
        shallow, mid = ocean[:len(ocean) // 3], ocean[len(ocean) // 3: 2 * len(ocean) // 3]
        sets = dict(grass=ground_tiles('Tileset_Ground_GroundGrass'),
                    snow=ground_tiles('Tileset_Ground_GroundSnow'),
                    sand=ground_tiles('Tileset_Ground_SandShore'),
                    rock=ground_tiles('Tileset_Ground_GroundRock'))
        light, dark = ground_tiles('Tileset_Grass_Light'), ground_tiles('Tileset_Grass_Dark')
        over = dict(snow=ground_tiles('Tileset_Ground_SnowOverlay'),
                    sand=ground_tiles('Tileset_Ground_SandOverlay'))
        n = Noise(self.seed + 5, 34)

        ring1, ring2 = self.grow(land), self.grow(self.grow(land))
        mask = Image.new('L', (self.W, self.H), 0)

        def paint(c, r, tile, to_mask=False):
            img.alpha_composite(tile, self.hexpos(c, r))
            if to_mask:
                mask.paste(255, self.hexpos(c, r), tile.getchannel('A'))

        for c, r in self.cells():
            if ring2[r][c] and not ring1[r][c]:
                paint(c, r, rnd.choice(mid))
        for c, r in self.cells():
            if ring1[r][c] and not land[r][c]:
                paint(c, r, rnd.choice(shallow))
        for c, r in self.cells():
            x, y = self.center(c, r)
            if ring1[r][c] and not land[r][c] and beach_fn and beach_fn(x, y):
                if any(land[b][a] for a, b in self.nbrs(c, r)):
                    paint(c, r, rnd.choice(sets['sand']))
        for c, r in self.cells():
            if land[r][c]:
                x, y = self.center(c, r)
                z = zone_fn(x, y)
                paint(c, r, rnd.choice(sets[z]), True)
                k = n(x * 1.7, y * 1.7)
                if z == 'grass' and k > 0.7:
                    paint(c, r, rnd.choice(light))
                elif z == 'grass' and k < 0.22:
                    paint(c, r, rnd.choice(dark))
                elif z in over and k > 0.5:
                    paint(c, r, rnd.choice(over[z]))
        for tiles, cx, cy, rx, ry, chance in decals:
            for c, r in self.cells():
                x, y = self.center(c, r)
                if land[r][c] and math.hypot((x - cx) / rx, (y - cy) / ry) < 1 and rnd.random() < chance:
                    paint(c, r, rnd.choice(tiles))
        return mask


# ---------------------------------------------------------------- sprites

def comps(im, gap=2):
    """Bounding boxes of separate sprites on a sheet, in reading order."""
    Wd, Hd = im.size
    a = im.getchannel('A').load()
    seen = set()
    boxes = []
    for y in range(Hd):
        for x in range(Wd):
            if a[x, y] and (x, y) not in seen:
                st = [(x, y)]
                seen.add((x, y))
                x0 = x1 = x
                y0 = y1 = y
                while st:
                    cx, cy = st.pop()
                    x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
                    for dy in range(-gap, gap + 1):
                        for dx in range(-gap, gap + 1):
                            p = (cx + dx, cy + dy)
                            if 0 <= p[0] < Wd and 0 <= p[1] < Hd and p not in seen and a[p]:
                                seen.add(p)
                                st.append(p)
                boxes.append((x0, y0, x1 + 1, y1 + 1))
    boxes.sort(key=lambda b: (b[1] // 16, b[0]))
    return boxes


def sheet_sprites(path, ids):
    im = tex(*path)
    bs = comps(im)
    return [im.crop(bs[i]) for i in ids]


def files(folder, prefix, nums):
    return [tex(folder, f'{prefix}{n}.png') for n in nums]


def load_sprites():
    S = {}
    m = ('Tileset_Rocks', 'Tileset_Rock_Mountains.png')
    S['mtn_brown'] = sheet_sprites(m, [8, 6, 7, 5, 3, 12])
    S['mtn_green'] = sheet_sprites(m, [21, 19, 20, 18, 16, 25])
    S['mtn_snowcap'] = sheet_sprites(m, [34, 32, 33, 31, 29, 38])
    S['mtn_snow'] = sheet_sprites(m, [47, 45, 46, 44, 42, 51])
    S['hills'] = sheet_sprites(m, [9, 10, 22, 23])
    c = ('Tileset_Buildings', 'Tileset_Buildings_Castles.png')
    S['castle_big'], S['castle_white'], S['castle_white2'], S['keep_orange'], S['keep_dark'], \
        S['tower_orange'], S['tower_white'], S['ruin'] = sheet_sprites(c, [8, 7, 9, 6, 34, 0, 2, 13])
    v = ('Tileset_Buildings', 'Tileset_Buildings_Village.png')
    S['village_orange'] = sheet_sprites(v, [4, 5, 17, 10, 11, 8, 2, 3, 14])
    S['village_dark'] = sheet_sprites(v, [39, 40])
    S['cathedral'] = sheet_sprites(v, [58])[0]
    S['spire'] = sheet_sprites(v, [43])[0]
    S['village_desert'] = sheet_sprites(v, [72, 73, 65, 66, 28, 29])
    S['palace'] = sheet_sprites(v, [84, 85])
    S['minaret'] = sheet_sprites(v, [86])[0]
    S['lighthouse'] = sheet_sprites(('Tileset_Buildings', 'Tileset_Buildings_Lighthouses.png'), [0])[0]
    veg = 'Standalone_Vegetation'
    S['pine'] = files(veg, 'Standalone_Tree_Pine', [1, 6, 2, 3, 4, 9])
    S['pine_snow'] = files(veg, 'Standalone_Tree_PineSnow', [1, 2, 6, 7, 8])
    S['beech'] = files(veg, 'Standalone_Tree_Beech', [1, 2, 3, 5, 6, 8, 9, 12, 13])
    S['oak'] = files(veg, 'Standalone_Tree_Oak', [1, 2, 3, 4])
    S['poplar'] = files(veg, 'Standalone_Tree_Poplar', [4, 5, 6, 7, 8, 9])
    S['palm'] = files(veg, 'Standalone_Tree_Palm', [1, 2, 3, 5, 6, 8])
    S['bush'] = files(veg, 'Standalone_Tree_Bush', [2, 3, 4, 5, 6])
    S['cactus'] = files(veg, 'Standalone_Tree_Cactus', [2, 3, 4, 5, 6, 7])
    S['field'] = files(veg, 'Standalone_Field_Yellow', [1, 2, 3, 4]) + \
        files(veg, 'Standalone_Field_LightGreen', [1, 2, 3])
    S['flowers'] = files(veg, 'Standalone_Flowers_Light_Overlay', [1, 2, 3, 4, 5, 6, 7])
    rk = 'Standalone_Rocks'
    S['dunes'] = files(rk, 'Standalone_Rock_SandDunes', [1, 2, 3, 4, 5, 6])
    S['stones'] = files(rk, 'Standaline_Rock_Magic', [1, 2, 3, 4, 5, 6, 9, 10, 11])
    S['stone_circle'] = tex(rk, 'Standaline_Rock_Magic17.png')
    S['arch'] = files(rk, 'Standalone_Rock_Arch', [1, 2, 5, 6])
    S['boulders'] = files(rk, 'Standalone_Rock_Organ', [2, 3, 4, 6, 7, 8])
    b = 'Standalone_Buildings'
    S['mill'] = [tex(b, f).crop((0, 0, 16, 16)) for f in
                 ['Standalone_Mill_White&Wood.png', 'Standalone_Mill_White&Terracotta.png']]
    S['boat'] = [tex(b, f'Standalone_SailingBoat{i}_Sails{s}.png') for i in (1, 2) for s in ('White', 'Red')]
    S['treasure'] = files(b, 'Standalone_Treasure', [2, 3])
    S['bridge'] = tex(b, 'Standalone_Buildings_Bridges5.png')
    S['galleon'] = tex('Ship', 'GalleonShip_East_SailsWhite.png').crop((0, 0, 32, 32))
    S['galleon_ne'] = tex('Ship', 'GalleonShip_NorthEast_SailsWhite.png').crop((0, 0, 32, 32))
    cr = 'Standalone_Creatures'
    S['kraken'] = tex(cr, 'Standalone_Creatures_Kraken.png')
    S['serpent'] = tex(cr, 'Standalone_Creatures_SnakeVeryBig.png')
    S['nessy'] = tex(cr, 'Standalone_Creatures_Nessy.png')
    S['lake_serpent'] = tex(cr, 'Standalone_Creatures_SnakeBig.png')
    S['dragon'] = tex(cr, 'Standalone_Creatures_Dragon2.png')
    S['sheep'] = files(cr, 'Standalone_Creatures_Sheeps', [1, 2, 3])
    S['crab'] = tex(cr, 'Standalone_Creatures_CrabBig.png')
    S['rose'] = tex('Parchment&WindRoses', 'WindRoses', 'Standalone_WindRose_ReadyMade9.png')
    S['swamp'] = decal_tiles('Tileset_Ground', 'Tileset_Ground_SwampOverlay')
    return S


def mirror(im):
    return ImageOps.mirror(im)


class Placer:
    """Collects sprites, avoids collisions, then draws them back to front."""

    def __init__(self, mask):
        self.W, self.H = mask.size
        self.mask = mask.load()
        self.items = []   # (bottom_y, left, top, image)
        self.solid = []   # boxes that scattered sprites must avoid

    def on_land(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H and self.mask[int(x), int(y)] > 0

    def fits(self, box, pad=0):
        x0, y0, x1, y1 = box
        return all(x1 + pad <= a or x0 - pad >= c or y1 + pad <= b or y0 - pad >= d
                   for a, b, c, d in self.solid)

    def put(self, im, x, y, solid=True):
        """Place sprite with its bottom-center at (x, y)."""
        left, top = int(x - im.width / 2), int(y - im.height)
        self.items.append((y, left, top, im))
        if solid:
            self.solid.append((left, top, left + im.width, top + im.height))

    def put_near(self, im, x, y, reach=48):
        """Place a landmark at the closest free spot on land to (x, y). Returns the spot."""
        for d in range(0, reach, 2):
            for k in range(max(1, d * 2)):
                a = k / max(1, d * 2) * math.tau
                px, py = x + math.cos(a) * d, y + math.sin(a) * d
                box = (int(px - im.width / 2), int(py - im.height), int(px + im.width / 2), int(py))
                feet = [(box[0] + 1, py - 1), (box[2] - 1, py - 1), (px, py - 1),
                        (box[0] + 1, box[1] + 2), (box[2] - 1, box[1] + 2)]
                if all(self.on_land(*q) for q in feet) and self.fits(box):
                    self.put(im, px, py)
                    return px, py
        return None

    def keep_out(self, box):
        self.solid.append(box)

    def scatter(self, rnd, choices, cx, cy, rx, ry, count, tries=600, land=True, pad=1, solid=True):
        placed = []
        for _ in range(tries):
            if len(placed) >= count:
                break
            a, d = rnd.random() * math.tau, math.sqrt(rnd.random())
            x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
            im = rnd.choice(choices)
            box = (int(x - im.width / 2), int(y - im.height), int(x + im.width / 2), int(y))
            feet = [(box[0] + 2, y - 1), (box[2] - 2, y - 1), (x, y - 1), (x, box[1] + im.height / 2)]
            if land and not all(self.on_land(*p) for p in feet):
                continue
            if not land and any(self.on_land(*p) for p in feet + [(box[0], box[1]), (box[2], box[1])]):
                continue
            if not self.fits(box, pad):
                continue
            self.put(im, x, y, solid)
            placed.append((im, x, y))
        return placed

    def forest(self, rnd, choices, cx, cy, rx, ry, count):
        """Dense trees: they may overlap each other but not other sprites."""
        trees = []
        for _ in range(count * 8):
            if len(trees) >= count:
                break
            a, d = rnd.random() * math.tau, math.sqrt(rnd.random())
            x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
            im = rnd.choice(choices)
            box = (int(x - im.width / 2 + 4), int(y - im.height + 6), int(x + im.width / 2 - 4), int(y))
            if not (self.on_land(x, y - 2) and self.on_land(box[0], y - 2) and self.on_land(box[2], y - 2)):
                continue
            if not self.fits(box) or any(math.hypot(x - tx, y - ty) < 9 for _, tx, ty in trees):
                continue
            trees.append((im, x, y))
            self.put(im, x, y, solid=False)
        self.solid += [(int(x - 8), int(y - 16), int(x + 8), int(y)) for _, x, y in trees]
        return trees

    def draw(self, img):
        for _, left, top, im in sorted(self.items, key=lambda t: t[0]):
            img.alpha_composite(im, (left, top))


# ---------------------------------------------------------------- labels

def banner(text, fnt, style=3, scale=1):
    """A parchment ribbon stretched to fit the text. style 3 = forked, 1 = curled."""
    base = os.path.join('Parchment&WindRoses', 'Parchments')
    L = tex(base, f'Standalone_Parchment{style}_PartLeft.png')
    C = tex(base, f'Standalone_Parchment{style}_PartCenter.png')
    R = tex(base, f'Standalone_Parchment{style}_PartRight.png')
    inner = max(int(fnt.getlength(text)) + 2, 8)
    w = L.width + inner + R.width
    im = Image.new('RGBA', (w, L.height))
    x = L.width
    while x < L.width + inner:
        im.alpha_composite(C.crop((0, 0, min(C.width, L.width + inner - x), C.height)), (x, 0))
        x += C.width
    im.alpha_composite(L, (0, 0))
    im.alpha_composite(R, (L.width + inner, 0))
    rows = [y for y in range(C.height) if C.getpixel((C.width // 2, y))[3]]
    band = (rows[0] + rows[-1]) / 2 if rows else C.height / 2
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    bb = d.textbbox((0, 0), text, font=fnt)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], band - (bb[1] + bb[3]) / 2), text, font=fnt, fill=INK)
    im = im.crop(im.getbbox())
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST) if scale > 1 else im


def caption(text, fnt, color=PALE, outline=(40, 46, 60, 255)):
    """Pixel text with a 1px outline, for subtitles on the map."""
    probe = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    probe.fontmode = '1'
    bb = probe.textbbox((0, 0), text, font=fnt)
    w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
    im = Image.new('RGBA', (w, h))
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            d.text((2 - bb[0] + dx, 2 - bb[1] + dy), text, font=fnt, fill=outline)
    d.text((2 - bb[0], 2 - bb[1]), text, font=fnt, fill=color)
    return im


def frame(img):
    """Pale zig-zag border like an old chart."""
    W, H = img.size
    d = ImageDraw.Draw(img)
    pale = (226, 232, 242, 255)
    m = 10
    for box in ([0, 0, W - 1, m - 1], [0, H - m, W - 1, H - 1], [0, 0, m - 1, H - 1], [W - m, 0, W - 1, H - 1]):
        d.rectangle(box, fill=DEEP)
    for x in range(m, W - m, 6):
        for y0, s in ((m, 1), (H - m - 1, -1)):
            d.line([(x, y0), (x + 3, y0 + 3 * s), (x + 6, y0)], fill=pale)
    for y in range(m, H - m, 6):
        for x0, s in ((m, 1), (W - m - 1, -1)):
            d.line([(x0, y), (x0 + 3 * s, y + 3), (x0, y + 6)], fill=pale)


def curve(pts, step=2):
    """Points along a Catmull-Rom curve through pts, about `step` px apart."""
    def cr(p0, p1, p2, p3, t):
        return tuple(0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - e) * t * t +
                            (-a + 3 * b - 3 * c + e) * t ** 3) for a, b, c, e in zip(p0, p1, p2, p3))
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        n = max(1, int(math.dist(P[i], P[i + 1]) / step))
        out += [cr(P[i - 1], P[i], P[i + 1], P[i + 2], s / n) for s in range(n)]
    return out


def trail(img, placer, pts, on_land=True, color=(122, 92, 58, 255), dash=(2, 4)):
    """Dotted trail through pts, drawn only on land (or only on water)."""
    d = ImageDraw.Draw(img)
    for k, (x, y) in enumerate(curve(pts)):
        if k % dash[1] < dash[0] and placer.on_land(x, y) == on_land:
            d.rectangle([int(x), int(y), int(x) + 1, int(y) + 1], fill=color)


def write_data(path, data, generator):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'// Generated by {generator}. Do not edit by hand.\n')
        f.write('window.MAP_DATA = ' + json.dumps(data, indent=2) + ';\n')
