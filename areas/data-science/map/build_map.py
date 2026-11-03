"""Build the Data Science region map: a close-up of the overworld's western region.

The land comes from the overworld's own terrain (map/build_world.py), magnified, so the coast,
river, and borders match what students see on the Computation Quests map.

Usage (from the repo root):
    python areas/data-science/map/build_map.py

Writes map.png and map-data.js next to this script.
"""
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'map'))
import build_world  # noqa: E402
import maplib as ml  # noqa: E402

TITLE = 'Data Science'
COLS, ROWS, SEED = 52, 72, 7
X0, Y0, ZOOM = 40, 164, 2   # overworld pixel at this map's top-left, and magnification

# Places along the data investigation cycle. `at` is where the landmark goes; the banner sits
# above it. Change names and copy here; the map and page follow.
PLACES = [
    dict(id='asking-questions', name='Asking Questions', step='Ask', at=(560, 150),
         idea='The data investigation cycle',
         text='Every investigation starts with a question that data can answer. Students learn to '
              'tell statistical questions from ones that are not, and to sharpen a vague wondering '
              'into something they can investigate.'),
    dict(id='sampling', name='Sampling', step='Sample', at=(420, 286),
         idea='Data is collected for a purpose',
         text='You cannot measure everything. Students learn how a sample represents a population, '
              'and how a biased sample leads to the wrong answer.'),
    dict(id='data-collection', name='Data Collection', step='Collect', at=(300, 440),
         idea='Data is collected for a purpose',
         text='Data arrives from surveys, sensors, and the web. Students collect their own data and '
              'ask who gathered it, how, and what was left out.'),
    dict(id='outliers', name='Outliers', step='Question', at=(44, 512),
         idea='Data must be organized and cleaned',
         text='A lone tower far from the rest. Students decide whether an outlier is an error to fix '
              'or a discovery to explain.'),
    dict(id='data-cleaning', name='Data Cleaning', step='Clean', at=(400, 752),
         idea='Data must be organized and cleaned',
         text='Typos, missing values, and duplicates hide in the marsh. Students learn to spot and '
              'fix messy data before it misleads them.'),
    dict(id='organizing-data', name='Organizing Data', step='Organize', at=(486, 612),
         idea='Data must be organized and cleaned',
         text='Rows, columns, and data types keep the town in order. Students structure data so a '
              'computer can work with it.'),
    dict(id='exploring-data', name='Exploring Data', step='Explore', at=(560, 444),
         idea='Patterns and models help us predict',
         text='Trends emerge from the forest. Students summarize data and look for patterns, '
              'clusters, and relationships.'),
    dict(id='visualization', name='Visualization', step='Visualize', at=(744, 300),
         idea='Visualizations tell stories, and can mislead',
         text='Windmills turn data into charts. Students choose the right chart for the story and '
              'learn to catch graphs that mislead.'),
    dict(id='modeling', name='Modeling', step='Model', at=(766, 486),
         idea='Patterns and models help us predict',
         text='Climb from simple trend lines to computational models. Students build models, test '
              'them, and see where they break.'),
    dict(id='prediction', name='Prediction', step='Predict', at=(806, 650),
         idea='Patterns and models help us predict',
         text='The watchtower looks ahead. Students make predictions from models and learn to '
              'express how uncertain they are.'),
    dict(id='interpreting-results', name='Interpreting Results', step='Interpret', at=(690, 778),
         idea='The data investigation cycle',
         text='Where findings are weighed and shared. Students make claims backed by evidence and '
              'communicate them to an audience.'),
    dict(id='privacy-and-fairness', name='Privacy and Fairness', step='Reflect', at=(804, 850),
         idea='Data has consequences',
         text='The road east leads on to Ethics and Impacts. Students weigh privacy, consent, and '
              'fairness in how data is collected and used.'),
]
# Neighboring regions, labeled at the map's edges: (text, x, y)
NEIGHBORS = [('AI Literacy', 640, 22), ('Ethics and Impacts', 744, 846)]


def to_world(x, y):
    return X0 + x / ZOOM, Y0 + y / ZOOM


def main():
    hm = ml.HexMap(COLS, ROWS, SEED)
    W, H, rnd = hm.W, hm.H, hm.rnd
    img = Image.new('RGBA', (W, H), ml.DEEP)
    wland, wzone, wbeach = build_world.world_terrain()
    fine = ml.Noise(SEED, 24)

    def land(x, y):
        v = wland(*to_world(x, y))
        return v if v < 0 else v + (fine(x, y) - 0.5) * 0.12

    S = ml.load_sprites()
    light, dark = ml.ground_tiles('Tileset_Grass_Light'), ml.ground_tiles('Tileset_Grass_Dark')
    mask = hm.terrain(img, land, lambda x, y: wzone(*to_world(x, y)), lambda x, y: wbeach(*to_world(x, y)),
                      decals=[(S['swamp'], 400, 740, 110, 60, 0.75),
                              (dark, 330, 590, 90, 80, 0.6), (dark, 560, 430, 70, 60, 0.6),
                              (light, 740, 320, 90, 60, 0.5), (light, 420, 290, 80, 40, 0.5)],
                      edge=0)
    pl = ml.Placer(mask)
    f16 = ml.font(16)

    title = ml.banner(TITLE, f16, style=1, scale=2)
    tpos = (150 - title.width // 2, 790)
    pl.keep_out((tpos[0], tpos[1], tpos[0] + title.width, tpos[1] + title.height))
    rose_at = (40, 600)
    pl.keep_out((rose_at[0], rose_at[1], rose_at[0] + 142, rose_at[1] + 142))
    edges = []
    for text, x, y in NEIGHBORS:
        cap = ml.caption(text, f16)
        pos = (x - cap.width // 2, y - cap.height // 2)
        edges.append((cap, pos))
        pl.keep_out((pos[0], pos[1], pos[0] + cap.width, pos[1] + cap.height))

    # Landmarks for each place. Each returns the spot its banner should sit above.
    spots = {}
    P = {p['id']: p['at'] for p in PLACES}

    def at(pid, im, dx=0, dy=0, reach=48):
        x, y = P[pid]
        return pl.put_near(im, x + dx, y + dy, reach)

    spots['asking-questions'] = at('asking-questions', S['tower_orange'])
    at('asking-questions', S['stone_circle'], 40, 6)

    spots['sampling'] = at('sampling', S['village_orange'][3])
    for dx, dy in [(-34, 10), (30, 12), (-10, 30), (40, -12), (-40, -14)]:
        at('sampling', rnd.choice(S['field']), dx, dy, 20)

    spots['data-collection'] = at('data-collection', S['village_orange'][1])
    for dx, dy in [(-26, 14), (22, 16), (0, 32), (-40, -6)]:
        at('data-collection', rnd.choice(S['village_orange']), dx, dy, 24)

    spots['outliers'] = at('outliers', S['tower_white'], reach=30)

    spots['data-cleaning'] = at('data-cleaning', S['village_dark'][0])
    pl.scatter(rnd, S['bush'], 400, 740, 100, 50, 24, pad=0)

    # Organizing Data: houses laid out in tidy rows around a spire.
    ox, oy = P['organizing-data']
    spots['organizing-data'] = at('organizing-data', S['spire'])
    for row in range(2):
        for col in range(4):
            pl.put_near(S['village_orange'][5], ox - 48 + col * 32, oy + 22 + row * 18, 6)

    spots['exploring-data'] = at('exploring-data', S['treasure'][1])
    pl.forest(rnd, S['beech'] + S['oak'], 550, 430, 60, 50, 60)

    spots['visualization'] = at('visualization', rnd.choice(S['mill']))
    for dx, dy in [(-30, 16), (28, 10), (4, 34), (52, 30)]:
        at('visualization', rnd.choice(S['mill']), dx, dy, 20)
    pl.scatter(rnd, S['field'], 744, 330, 70, 40, 10)

    spots['modeling'] = at('modeling', S['mtn_green'][0])
    pl.scatter(rnd, S['mtn_green'] + S['mtn_brown'][:3], 770, 470, 60, 50, 10)

    spots['prediction'] = at('prediction', S['tower_white'])
    pl.scatter(rnd, S['hills'], 800, 660, 40, 30, 4)

    ix, iy = P['interpreting-results']
    spots['interpreting-results'] = at('interpreting-results', S['castle_white'])
    for t in range(6):
        a = t * math.tau / 6
        pl.put_near(rnd.choice(S['village_orange']), ix + math.cos(a) * 40, iy + 10 + math.sin(a) * 22, 14)

    spots['privacy-and-fairness'] = at('privacy-and-fairness', S['keep_orange'])

    # Banners above their landmarks.
    labels = {}
    for p in PLACES:
        b = ml.banner(p['name'], f16)
        sx, sy = spots[p['id']] or p['at']
        x, y = int(sx - b.width / 2), int(sy - 44 - b.height / 2)
        x = max(12, min(W - 12 - b.width, x))
        y = max(12, y)
        box = (x, y, x + b.width, y + b.height)
        labels[p['id']] = (b, box)
        pl.keep_out(box)

    # The north: AI Literacy's snowy foothills.
    pl.scatter(rnd, S['mtn_snow'][:4], 600, 40, 260, 40, 12)
    pl.scatter(rnd, S['mtn_snowcap'], 560, 90, 300, 40, 12)
    pl.forest(rnd, S['pine_snow'], 420, 70, 120, 30, 30)
    pl.forest(rnd, S['pine'], 400, 180, 140, 30, 50)

    # Forests, hills, and countryside.
    pl.forest(rnd, S['beech'] + S['oak'], 330, 600, 80, 70, 110)
    pl.forest(rnd, S['pine'], 300, 260, 80, 40, 40)
    pl.forest(rnd, S['pine'] + S['beech'], 690, 560, 40, 50, 40)
    pl.forest(rnd, S['pine'], 640, 250, 60, 30, 40)
    pl.forest(rnd, S['oak'] + S['beech'], 460, 360, 50, 30, 30)
    for vx, vy in [(520, 250), (660, 340), (360, 340), (640, 700), (520, 820)]:
        pl.scatter(rnd, S['village_orange'][5:], vx, vy, 20, 12, 2)
    pl.forest(rnd, S['oak'] + S['poplar'], 600, 760, 50, 40, 30)
    pl.scatter(rnd, S['hills'], 500, 300, 160, 120, 14)
    pl.scatter(rnd, S['sheep'], 640, 330, 60, 40, 4)
    pl.scatter(rnd, S['bush'], 520, 480, 340, 400, 90, pad=2)

    # Sea.
    pl.put(S['galleon'], 190, 470)
    pl.put(S['serpent'], 110, 300)
    pl.put(S['kraken'], 216, 580)
    pl.scatter(rnd, S['boat'], 130, 400, 120, 300, 6, land=False, pad=14)

    # The trail follows the cycle and leaves east toward Ethics and Impacts; bridges where it
    # crosses the river.
    trail = [spots[p['id']] or p['at'] for p in PLACES if p['id'] != 'outliers']
    trail = [(x, y + 4) for x, y in trail] + [(W, 880)]
    ml.trail(img, pl, trail)
    pts = ml.curve(trail)
    for a, b in zip(pts, pts[1:]):
        if pl.on_land(*a) and not pl.on_land(*b):
            for c in pts[pts.index(b):]:
                if pl.on_land(*c):
                    mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
                    pl.put(S['bridge'], mx, my + 8, solid=False)
                    break
    ml.trail(img, pl, [P['outliers'], (130, 500), spots['data-collection']], on_land=False,
             color=(226, 232, 242, 255), dash=(3, 6))

    pl.draw(img)
    for b, box in labels.values():
        img.alpha_composite(b, box[:2])
    for cap, pos in edges:
        img.alpha_composite(cap, pos)
    img.alpha_composite(title, tpos)
    img.alpha_composite(S['rose'], rose_at)
    ml.frame(img)
    img.save(os.path.join(HERE, 'map.png'))

    data = dict(title=TITLE, width=W, height=H, regions=[
        dict({k: p[k] for k in ('id', 'name', 'step', 'idea', 'text')}, box=labels[p['id']][1])
        for p in PLACES])
    ml.write_data(os.path.join(HERE, 'map-data.js'), data, 'areas/data-science/map/build_map.py')
    print(f'map.png {W}x{H}, {len(PLACES)} places')


if __name__ == '__main__':
    main()
