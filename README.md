# Computation Quests

**Computation Quests** is a free collection of **unplugged** activities for middle and high
school teachers teaching computer science, data science, computational thinking, cybersecurity,
and AI literacy. Every activity works with no technology: students use paper, cards, and each
other.

Computation Quests is one map, a continent divided into regions. Each region is a subject area
with unplugged activities, each with a teacher guide and print-ready handouts. Teachers browse the
map on the website; students never need a device.

> Status: **Planning / early content collection.** The first region with content is
> **Data Science**.

## Regions

| Region | Notes |
|---|---|
| **Computational Thinking** | The starting point, in the south |
| **Algorithms and Coding** | East |
| **Data Science** | West |
| **AI Literacy** | The snowy north |
| **Cybersecurity** | An island off the west coast |
| **Ethics and Impacts** | The center, where every road meets |

## Principles

- **Free.** Every activity and resource is free to use.
- **Unplugged.** No activity requires students to use technology. Teachers may print handouts.
- **No student data.** No accounts, and nothing is collected about anyone.
- **Teacher-friendly.** Activities are written so a teacher new to the topic can teach them.
- **Openly licensed.** Content is shared under CC BY-NC-SA 4.0 so teachers can adapt and remix it.

## Repository layout

```
index.html            The website's home page: the Computation Quests map
about/, 404.html      Other website pages
assets/site.css       Shared website styles
map/                  The overworld map: generator, image, and data
tools/build_pages.py  Generates the region pages and the shared header and footer
areas/                One folder per region, named by subject
  data-science/
    map/              The Data Science region map
    activities/       One folder per unplugged activity: teacher guide and printables
    resources/        Teacher background reading and related collections
docs/                 Project planning: vision, roadmap, decisions, area template
templates/            Copy-and-fill templates for activities and resources
inbox/                Drop zone for existing materials before they are sorted into a region
```

## Where to start

- [The website](#the-website): the map and region pages (see [map/README.md](map/README.md) to rebuild maps)
- [Vision](docs/vision.md): who this is for and what it is
- [Roadmap](docs/roadmap.md): phased plan
- [Area template](docs/area-template.md): the structure every region follows
- [Decisions](docs/decisions.md): decisions made so far and open questions

## The website

The site is plain HTML and CSS with no build tool. The home page is `index.html` at the repo root.

**Preview it locally** from the repo root, then open http://localhost:8765/:

```bash
python -m http.server 8765
```

**Change it:**

- Region names, descriptions, and topics: edit `REGIONS` in `map/build_world.py`, then run
  `python map/build_world.py` (needs the tile pack) and `python tools/build_pages.py`.
- A region page's extra section: edit `areas/<region>/extra.html`, then run
  `python tools/build_pages.py`.
- The home, About, and region map pages are hand-written HTML. Their header and footer are
  refreshed by `python tools/build_pages.py`; edit those in the script, not in the pages.

**Publish it (not done yet).** The site is ready for GitHub Pages but is not live. When you are
ready: on GitHub, open **Settings → Pages**, set **Source** to *Deploy from a branch*, choose
`main` and `/ (root)`, and save. The site will appear at https://mrenne.github.io/csworlds/. The
empty `.nojekyll` file tells Pages to serve the files as they are. If you later use a custom
domain, change `BASE` in `tools/build_pages.py` to `/` and rerun it.

Note that the repository itself is public, so its files can already be read on GitHub even
before the site is published.

## License

Unless otherwise noted, all content in this repository is licensed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)
(CC BY-NC-SA 4.0). See [LICENSE](LICENSE).

The map tile art comes from the La Petite Tile Maps pack and is **not** covered by this license
or included in the repository. See [map/README.md](map/README.md).

To attribute, use something like:

> "Activity Title" from Computation Quests by Mike Renne, licensed under CC BY-NC-SA 4.0.
> https://github.com/mrenne/csworlds
