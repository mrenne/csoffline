# CS Worlds

**CS Worlds** is a free collection of **unplugged** activities for middle and high school
teachers. Every activity works with no technology: students use paper, cards, and each other.

> Status: **planning, starting over** (November 2026). Only the decisions below are settled.

## Decided

| Decision | Notes |
|---|---|
| Name: **CS Worlds** | |
| Every activity is **unplugged** | Students use no technology. Teachers may print handouts |
| Topic focus: **computer science, computational thinking, data science, AI literacy, cybersecurity, and ethics** | |
| Audience: **middle and high school** (grades 6–12) | |
| Everything is **free** | |
| License: **CC BY-NC-SA 4.0** | See [LICENSE](LICENSE) |

## System

CS Worlds will be a website where students and educators explore the topics through unplugged
games. Worlds are microworlds (settings students explore), games are played inside them, and
concepts connect the games. See the [system spec](docs/system-spec.md) for the content model,
site structure, technical design, phases, and open decisions.

## Working on the site

The site is built with [Astro](https://astro.build/). You need Node.js 22 or later.

```bash
npm install
```

```bash
npm run dev
```

Then open http://localhost:4321/csworlds/. Content lives in `src/content/` (see the
[system spec](docs/system-spec.md), section 5). The build checks the content and stops with a
message if something is broken:

```bash
npm run build
```

The site is **not live**. GitHub Actions builds it on every push, but only deploys when started by
hand, after GitHub Pages is turned on (see `.github/workflows/site.yml`).

Current content is placeholder: the six topics, five sample concepts, and two placeholder worlds
and games standing in for the AI literacy and data science card games.

## Archive

An earlier version of this project, **Computation Quests**, is saved on the
`archive/computation-quests` branch (tag `archive-computation-quests`). It has a pixel-art map
of subject regions, a static website, map generators, templates, and unplugged activity ideas for
each topic. Nothing from it carries over unless it is brought back on purpose. To look at it:

```bash
git switch archive/computation-quests
```

## License

Unless otherwise noted, all content in this repository is licensed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)
(CC BY-NC-SA 4.0).
