"""Build the Computation Quests overworld map: one continent divided into regions, plus an island.

Usage (from the repo root):
    python map/build_world.py

Writes world.png and world-data.js next to this script.
"""
import math
import os

from PIL import Image

import maplib as ml

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = 'Computation Quests'

# Regions. Change names and copy here; the map and page follow.
REGIONS = [
    dict(id='computational-thinking', name='Computational Thinking', start=True, banner=(486, 884),
         text='The starting point. Students learn to break problems into parts, recognize '
              'patterns, focus on what matters, and describe solutions as clear steps.',
         topics=['Decomposition', 'Pattern recognition', 'Abstraction', 'Algorithmic thinking']),
    dict(id='algorithms-and-coding', name='Algorithms and Coding', banner=(700, 420),
         text='Students design, write, test, and debug programs, from first sequences and loops '
              'to complete projects.',
         topics=['Sequences, loops, and conditionals', 'Variables and data types', 'Functions',
                 'Testing and debugging', 'Program design']),
    dict(id='data-science', name='Data Science', banner=(292, 404), link='../areas/data-science/map/',
         text='Students ask questions, collect and clean data, look for patterns, build simple '
              'models, and communicate what the data shows.',
         topics=['Statistical questions', 'Collecting and cleaning data', 'Visualization',
                 'Models and prediction', 'Sampling and bias']),
    dict(id='ai-literacy', name='AI Literacy', banner=(470, 96),
         text='Students learn how AI systems learn from examples, where they succeed and fail, and '
              'how to evaluate what they produce.',
         topics=['How machine learning works', 'Training data', 'Generative AI', 'Evaluating AI output',
                 'Bias in AI systems']),
    dict(id='cybersecurity', name='Cybersecurity', banner=(124, 716),
         text='Students learn how systems and information are attacked and defended, from '
              'passwords and phishing to encryption.',
         topics=['Passwords and authentication', 'Social engineering', 'Encryption', 'Privacy',
                 'Networks and the internet']),
    dict(id='ethics-and-impacts', name='Ethics and Impacts', banner=(516, 560),
         text='At the center of the map, where every road meets. Students examine how computing '
              'affects individuals, communities, and society.',
         topics=['Bias and fairness', 'Privacy and surveillance', 'Accessibility',
                 'Computing and society', 'Responsible design']),
]

COLS, ROWS, SEED = 54, 104, 21

BLOBS = [
    # north (AI Literacy)
    (470, 190, 320, 118), (330, 284, 210, 90), (640, 300, 120, 80),
    # west (Data Science)
    (320, 470, 180, 136), (250, 400, 110, 80),
    # center (Ethics and Impacts) and east (Algorithms and Coding)
    (520, 590, 170, 140), (700, 520, 126, 150), (720, 380, 90, 70),
    # the neck and the south (Computational Thinking)
    (520, 730, 200, 110), (520, 890, 220, 130), (450, 1010, 170, 110), (560, 1090, 110, 70),
    (330, 940, 90, 80),
    # the western island (Cybersecurity)
    (122, 830, 78, 116, 0.6),
    # islets
    (60, 400, 22, 18), (830, 860, 20, 24), (250, 1160, 26, 18), (836, 640, 16, 18),
]
CARVE = [  # bays and gulfs: (cx, cy, rx, ry)
    (742, 760, 96, 64), (150, 640, 70, 46), (820, 980, 120, 90),
]
RIVERS = [  # polylines of water through the land
    [(440, 270), (400, 330), (360, 380), (300, 520), (230, 600), (150, 640)],
    [(700, 470), (660, 560), (690, 650), (742, 740)],
]


def seg_dist(p, a, b):
    ax, ay = a
    bx, by = b
    t = max(0, min(1, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
    return math.dist(p, (ax + t * (bx - ax), ay + t * (by - ay)))


def world_terrain():
    """The overworld's terrain functions, in world pixels. Region maps reuse these."""
    base = ml.blob_field(BLOBS, ml.Noise(SEED, 90), ml.Noise(SEED + 1, 34))
    zn = ml.Noise(SEED + 2, 60)
    wig = ml.Noise(SEED + 3, 40)

    def river(x, y):
        return any(min(seg_dist((x, y), a, b) for a, b in zip(line, line[1:])) < 10 + wig(x, y) * 5
                   for line in RIVERS)

    def land(x, y):
        for cx, cy, rx, ry in CARVE:
            if math.hypot((x - cx) / rx, (y - cy) / ry) < 1:
                return -1
        return -1 if river(x, y) else base(x, y)

    def zone(x, y):
        j = (zn(x, y) - 0.5) * 80
        if y < 196 + j:
            return 'snow'
        if y > 1060 + j:
            return 'sand'
        return 'grass'

    def beach(x, y):
        return not river(x, y) and (zn(x * 1.3, y * 1.3) > 0.5 or y > 1000)

    return land, zone, beach


def main():
    hm = ml.HexMap(COLS, ROWS, SEED)
    W, H, rnd = hm.W, hm.H, hm.rnd
    img = Image.new('RGBA', (W, H), ml.DEEP)
    land, zone, beach = world_terrain()

    S = ml.load_sprites()
    dark = ml.ground_tiles('Tileset_Grass_Dark')
    mask = hm.terrain(img, land, zone, beach, decals=[
        (S['swamp'], 250, 520, 60, 40, 0.7),
        (dark, 300, 330, 110, 50, 0.7), (dark, 230, 470, 60, 60, 0.6), (dark, 620, 330, 70, 40, 0.6),
        (dark, 400, 980, 70, 50, 0.6), (dark, 122, 840, 50, 60, 0.6),
    ])
    pl = ml.Placer(mask)
    f16 = ml.font(16)

    labels = {}
    for r in REGIONS:
        b = ml.banner(r['name'], f16)
        x, y = r['banner']
        box = (x - b.width // 2, y - b.height // 2, x - b.width // 2 + b.width, y - b.height // 2 + b.height)
        labels[r['id']] = (b, box)
        pl.keep_out(box)
    title = ml.banner(TITLE, f16, style=1, scale=2)
    tpos = (min(676 - title.width // 2, 872 - 28 - title.width), 1158)
    pl.keep_out((tpos[0], tpos[1], tpos[0] + title.width, tpos[1] + title.height))
    rose_at = (26, 540)
    pl.keep_out((rose_at[0], rose_at[1], rose_at[0] + 142, rose_at[1] + 142))

    # Ethics and Impacts: the walled city at the center, where the roads meet.
    city = (516, 640)
    pl.put_near(S['castle_big'], city[0], city[1] - 6)
    pl.put_near(S['castle_white'], city[0] - 26, city[1])
    pl.put_near(S['castle_white2'], city[0] + 28, city[1] + 2)
    pl.put_near(S['cathedral'], city[0], city[1] + 18)
    for t in range(10):
        a = t * math.tau / 10
        pl.put_near(rnd.choice(S['village_orange']), city[0] + math.cos(a) * 52, city[1] + 12 + math.sin(a) * 30, 20)
    pl.forest(rnd, S['oak'] + S['beech'], 420, 600, 40, 40, 26)
    pl.scatter(rnd, S['field'], 600, 650, 40, 30, 6)

    # Computational Thinking: farmland, villages, and the harbor where the journey starts.
    harbor = None
    for yy in range(840, 980, 2):
        for xx in range(560, 760, 2):
            if pl.on_land(xx, yy) and not pl.on_land(xx + 12, yy) and not pl.on_land(xx + 12, yy - 10) \
                    and pl.fits((xx - 8, yy - 18, xx + 4, yy)):
                d = math.dist((xx, yy), (720, 900))
                if harbor is None or d < harbor[0]:
                    harbor = (d, xx, yy)
    _, hx, hy = harbor
    pl.put(S['lighthouse'], hx - 4, hy)
    for vx, vy in [(hx - 24, hy + 4), (hx - 38, hy - 12)]:
        pl.put_near(rnd.choice(S['village_orange']), vx, vy, 30)
    pl.put_near(S['keep_orange'], 470, 940)
    for vx, vy in [(440, 950), (500, 956), (456, 972), (520, 930), (410, 930)]:
        pl.put_near(rnd.choice(S['village_orange']), vx, vy)
    for vx, vy in [(560, 1080), (590, 1092), (360, 1040), (320, 960)]:
        pl.put_near(rnd.choice(S['village_orange'][3:]), vx, vy)
    for mx, my in [(580, 990), (604, 1010), (560, 1016), (620, 980)]:
        pl.put_near(rnd.choice(S['mill']), mx, my)
    pl.scatter(rnd, S['field'], 590, 1000, 60, 40, 12)
    pl.scatter(rnd, S['sheep'], 420, 1030, 60, 30, 5)
    pl.forest(rnd, S['beech'] + S['oak'], 400, 980, 60, 46, 60)
    pl.forest(rnd, S['oak'] + S['poplar'], 640, 860, 40, 30, 20)
    pl.scatter(rnd, S['mtn_green'], 460, 790, 120, 40, 8)
    pl.scatter(rnd, S['hills'], 540, 800, 160, 50, 10)
    pl.scatter(rnd, S['dunes'], 500, 1100, 120, 30, 6)

    # Algorithms and Coding: mountains, quarries, and workshops.
    pl.put_near(S['keep_dark'], 700, 560)
    for vx, vy in [(672, 576), (728, 580), (690, 600), (740, 552)]:
        pl.put_near(rnd.choice(S['village_dark'] + S['village_orange'][:3]), vx, vy)
    for mx, my in [(760, 630), (740, 650), (780, 650)]:
        pl.put_near(rnd.choice(S['mill']), mx, my)
    pl.scatter(rnd, S['mtn_brown'], 716, 420, 100, 60, 18)
    pl.scatter(rnd, S['boulders'], 700, 470, 100, 40, 8)
    pl.forest(rnd, S['pine'], 640, 680, 50, 40, 40)
    pl.forest(rnd, S['pine'], 780, 520, 30, 60, 26)

    # Data Science: towns, mills, fields, and the marsh.
    pl.put_near(S['spire'], 300, 452)
    for vx, vy in [(280, 464), (316, 470), (296, 486), (336, 450)]:
        pl.put_near(rnd.choice(S['village_orange']), vx, vy)
    for mx, my in [(380, 480), (400, 500), (370, 510)]:
        pl.put_near(rnd.choice(S['mill']), mx, my)
    pl.scatter(rnd, S['field'], 390, 500, 40, 30, 6)
    pl.scatter(rnd, S['bush'], 250, 520, 60, 40, 14, pad=0)
    pl.forest(rnd, S['beech'] + S['oak'], 220, 440, 60, 60, 60)
    pl.forest(rnd, S['pine'], 330, 330, 110, 40, 70)

    # AI Literacy: snowfields, peaks, and the standing stones.
    pl.put_near(S['stone_circle'], 470, 200)
    pl.put_near(S['tower_white'], 520, 214)
    pl.put_near(S['keep_dark'], 600, 260)
    pl.scatter(rnd, S['stones'], 470, 210, 80, 40, 8)
    pl.scatter(rnd, S['mtn_snow'][:4], 470, 150, 280, 50, 22)
    pl.scatter(rnd, S['mtn_snowcap'], 470, 220, 300, 50, 18)
    pl.forest(rnd, S['pine_snow'], 300, 230, 100, 30, 40)
    pl.forest(rnd, S['pine_snow'], 660, 240, 80, 30, 30)

    # Cybersecurity: a fortified island watched by towers on its coast.
    pl.put_near(S['castle_white2'], 122, 830)
    pl.put_near(S['keep_orange'], 100, 850)
    for t in range(8):
        a = t * math.tau / 8
        pl.put_near(S['tower_white'], 122 + math.cos(a) * 56, 836 + math.sin(a) * 86, 24)
    pl.forest(rnd, S['pine'], 130, 900, 40, 40, 20)

    # Scattered detail across the continent.
    pl.scatter(rnd, S['bush'], 480, 650, 330, 460, 90, pad=2)
    pl.scatter(rnd, S['hills'], 480, 560, 300, 300, 14)
    pl.forest(rnd, S['pine'] + S['beech'], 400, 740, 60, 40, 40)
    pl.forest(rnd, S['pine'], 700, 380, 60, 30, 30)
    pl.scatter(rnd, S['mtn_snowcap'], 470, 240, 260, 30, 10)

    # Roads meet at the center; a sea lane runs to the island.
    road = (128, 96, 60, 255)
    for pts in [[(hx - 10, hy), (560, 900), (520, 800), city],
                [(470, 950), (520, 860)],
                [city, (420, 520), (310, 470)],
                [city, (620, 590), (700, 570)],
                [city, (500, 470), (480, 330), (480, 216)],
                [(470, 950), (340, 900), (300, 880)]]:
        ml.trail(img, pl, pts, color=road, dash=(3, 4))
    ml.trail(img, pl, [(300, 880), (220, 850), (190, 840)], on_land=False,
             color=(226, 232, 242, 255), dash=(3, 6))

    # Sea life and sailors.
    pl.put(S['galleon_ne'], hx + 46, hy - 16)
    pl.put(S['kraken'], 806, 1060)
    pl.put(S['serpent'], 60, 1100)
    pl.put(S['lake_serpent'], 528, 446)
    pl.put(rnd.choice([S['dragon']]), 820, 300)
    pl.scatter(rnd, S['boat'], W / 2, H / 2, W / 2 - 40, H / 2 - 40, 10, land=False, pad=14)

    pl.draw(img)
    for b, box in labels.values():
        img.alpha_composite(b, box[:2])
    img.alpha_composite(title, tpos)
    img.alpha_composite(S['rose'], rose_at)
    ml.frame(img)
    img.save(os.path.join(HERE, 'world.png'))

    data = dict(title=TITLE, width=W, height=H, regions=[
        dict({k: r.get(k) for k in ('id', 'name', 'text', 'topics', 'link', 'start')}, box=labels[r['id']][1])
        for r in REGIONS])
    ml.write_data(os.path.join(HERE, 'world-data.js'), data, 'map/build_world.py')
    print(f'world.png {W}x{H}, {len(REGIONS)} regions')


if __name__ == '__main__':
    main()
