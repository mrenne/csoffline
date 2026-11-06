# Decisions

A running log of project decisions. Add new entries at the top.

## Decided

| Date | Decision | Notes |
|---|---|---|
| 2026-11-03 | **Every activity is unplugged** | Students use no technology. Teachers may print handouts. Same topics and map; the activity, with its printables, is the unit of content. Replaces the earlier mix of lessons, browser activities, and unplugged activities. See [vision](vision.md) |
| 2026-11-03 | Overworld is **one continent of regions plus one island**, in the style of a classic fantasy map | Replaces the earlier spread-out archipelago |
| 2026-11-03 | Regions use **plain subject names** for now | Computational Thinking, Algorithms and Coding, Data Science, AI Literacy, Cybersecurity, Ethics and Impacts |
| 2026-11-03 | **Human-in-the-loop** is an unstated design principle | Students discover it through activities; no human-focused slogans in branding. See [vision](vision.md) |
| 2026-11-03 | Website: **plain static HTML on GitHub Pages**, served from the root of `main` | No build tool or third-party requests; `tools/build_pages.py` generates region pages from the map data. Pages is not turned on yet |
| 2026-11-03 | Name: **Computation Quests** | The name of the whole map and the project. The repository stays `csworlds` |
| 2026-11-03 | Area folders named by subject (`areas/data-science/`) | Folder names stay stable if display names change |
| 2026-11-03 | Map tile art: licensed for use | Mike Renne holds a license to use the La Petite Tile Maps pack in commercial and noncommercial projects, so the generated maps can be published on the site |
| 2026-11-03 | Map tile pack not committed | The license covers using the art, not sharing the raw pack; only the generated maps are committed |
| 2026-11-03 | Start with **Data Science** | Other regions follow after it is piloted |
| 2026-11-03 | Everything is **free** | |
| 2026-11-03 | **No student accounts** | Now automatic: students never use the site. The site collects no data about anyone |
| 2026-11-03 | License: **CC BY-NC-SA 4.0** | Applies to all content unless otherwise noted |

## Open questions

- **Names.** The region names and the place names inside regions (e.g., on the Data
  Science map) are placeholders to rework.
- **License for software code.** Creative Commons does not recommend CC licenses for software.
  The repo's own scripts (the map and page generators) might use a software license (e.g., MIT)
  while the activities stay CC BY-NC-SA 4.0.
- **Large files.** PDFs and slide decks can be large. Options: commit them directly (fine under
  ~50 MB each), use Git LFS, or host them elsewhere and link to them.
- **Existing plugged materials.** Slide decks, browser activities, and GitHub repos do not fit
  the unplugged format as they are. For each one: adapt its core idea into an unplugged activity,
  keep it as teacher background in `resources/`, or leave it out. The inbox tracks this.
- **Printables format.** Likely PDF for printing, with an editable source (e.g., Google Docs or
  Word) so teachers can adapt them. Decide which source format to keep in the repo.
- **Standards to tag.** CSTA K–12 CS Standards for sure; also AI4K12, ISTE, Common Core math,
  NGSS?
