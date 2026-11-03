# Decisions

A running log of project decisions. Add new entries at the top.

## Decided

| Date | Decision | Notes |
|---|---|---|
| 2026-11-03 | Overworld is **one continent of regions plus one island**, in the style of a classic fantasy map | Replaces the earlier spread-out archipelago |
| 2026-11-03 | Regions use **plain subject names** for now | Computational Thinking, Algorithms and Coding, Data Science, AI Literacy, Cybersecurity, Ethics and Impacts |
| 2026-11-03 | **Human-in-the-loop** is an unstated design principle | Students discover it through activities; no human-focused slogans in branding. See [vision](vision.md) |
| 2026-11-03 | Name: **Computation Quests** | The name of the whole map and the project. The repository stays `csworlds` |
| 2026-11-03 | Area folders named by subject (`areas/data-science/`) | Folder names stay stable if display names change |
| 2026-11-03 | Map tile pack not committed | The La Petite Tile Maps license likely forbids redistributing raw assets; generated maps are committed |
| 2026-11-03 | Start with **Data Science** | Other regions follow after it is piloted |
| 2026-11-03 | Everything is **free** | |
| 2026-11-03 | **No student accounts** | Student activities are anonymous and collect no PII |
| 2026-11-03 | License: **CC BY-NC-SA 4.0** | Applies to all content unless otherwise noted |

## Open questions

- **Names.** The region names and the place names inside regions (e.g., on the Data
  Science map) are placeholders to rework.
- **Tile pack license.** Confirm the La Petite Tile Maps terms allow publishing generated maps on a
  free educational site.
- **License for software code.** Creative Commons does not recommend CC licenses for software.
  Interactive activities and code from GitHub repos might use a software license (e.g., MIT or
  GPL) while lessons and documents stay CC BY-NC-SA 4.0.
- **Large files.** PDFs and slide decks can be large. Options: commit them directly (fine under
  ~50 MB each), use Git LFS, or host them elsewhere and link to them.
- **Existing GitHub repos.** Link to them from `resources/`, or bring their content into this
  repo (copy or git submodule).
- **Website stack.** To decide in Phase 2.
- **Standards to tag.** CSTA K–12 CS Standards for sure; also AI4K12, ISTE, Common Core math,
  NGSS?
