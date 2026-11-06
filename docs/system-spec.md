# CS Worlds system spec

> Status: **draft**, November 2026. Phase 2 core pages are built in Astro with placeholder content. This spec covers the system: the content model, the website,
> and how content is added. It does not cover the games or curriculum themselves, which are
> designed separately. Items marked **(open)** need a decision; see [Open decisions](#open-decisions).

## 1. Purpose

CS Worlds is a website where students and educators explore computer science through unplugged
games. Each game is played without technology. The website is where people find the games,
learn to play them, get the printables, and explore the ideas behind them.

The system unifies two ideas:

- **Microworlds:** settings with their own look, story, and simple rules, which students explore.
- **Game worlds:** unplugged games played inside those settings.

Games are connected by the **concepts** they teach, and concepts belong to **topics**. That web of
links is what makes a set of separate games into one system.

## 2. Principles

1. **Games are always unplugged.** No game may require the website or any device to play. The
   site supports the games; it is never part of the gameplay.
2. **No accounts, no student data.** No sign-in, no cookies, no analytics, no third-party
   requests. Anything personal, such as progress, stays in the visitor's own browser.
3. **Free and open.** All content is CC BY-NC-SA 4.0 unless noted.
4. **Content, not pages.** Every page is generated from structured content files. Adding a game
   means adding files, not building pages.
5. **Structure is checked.** The content model is enforced at build time; broken links between
   content fail the build instead of reaching the site.
6. **One content set, two views.** Students and educators see the same worlds, games, and
   concepts, presented for their needs.
7. **Accessible and fast.** WCAG 2.2 AA, usable on a phone or a school Chromebook, and readable on
   a classroom projector.

## 3. Users

| User | Goals | Typical entry point |
|---|---|---|
| **Student** (grades 6–12) | Find a world, learn a game's rules, understand "what's really going on" | The world map, or a link or QR code from a teacher or a printed card |
| **Educator** | Find a game for a topic or concept, prepare and print it, run and debrief it, plan a unit | The catalog, a topic or concept page, search |
| **Author** (the project team) | Add and update worlds, games, concepts, and printables | The content files in the repo |

Whether students use the site on their own or mainly through a teacher is **(open)**. The spec
assumes the student view must stand on its own.

## 4. Core concepts

```
Topic 1──* Concept *──* Game *──1 World
                          │
                          ├──* Printable
                          ├──* Variant
                          └──* Standard
Pathway *──* Game   (an ordered list)
```

| Term | Meaning |
|---|---|
| **Topic** | One of six fixed subject areas: Computer Science, Computational Thinking, Data Science, AI Literacy, Cybersecurity, Ethics |
| **Concept** | An idea a game teaches, such as training data, sampling, or encryption. Belongs to one or more topics |
| **World** | A microworld: a setting with a story, art, and rules of its own. Holds one or more games |
| **Game** | An unplugged game, such as a card game, board game, or role-play, set in one world |
| **Variant** | A named change to a game's rules, often to focus on a different concept or grade band |
| **Printable** | A file to print for a game: cards, boards, rules, log sheets |
| **Pathway** | An ordered sequence of games for a unit or course, written for educators |
| **Standard** | A standards statement, such as a CSTA code, that a game supports |

Whether a world may hold more than one game from the start is **(open)**; the model allows it.

## 5. Content model

Content lives in files under `src/content/`, as Markdown with YAML front matter. The body of each
file is free text; the front matter is checked against the schema below. Slugs come from file or
folder names and never change once published (they are the URLs).

### 5.1 Topic: `src/content/topics/<slug>.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Display name |
| `summary` | string | yes | One sentence |
| `color` | string | yes | Design token name, not a hex value |
| `icon` | string | yes | Icon name from the site's icon set |
| `order` | number | yes | Display order |

Body: a short introduction. Exactly six topic files exist; adding a seventh fails the build.

### 5.2 Concept: `src/content/concepts/<slug>.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `topics` | topic refs | yes | At least one |
| `student_summary` | string | yes | One or two sentences at a grade 6 reading level |
| `related` | concept refs | no | Shown as "see also" |
| `standards` | standard refs | no | |

Body sections, by heading:

- `## What's really going on`: for students; how the idea works in real systems
- `## Background`: for educators
- `## Misconceptions`: for educators

### 5.3 World: `src/content/worlds/<slug>/index.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `tagline` | string | yes | One line, shown on the map and cards |
| `art` | image | no | Hero image, in the same folder. Required once the visual identity is decided |
| `art_alt` | string | no | Alt text for the art |
| `map_position` | {x, y} | no | Where it sits on the world map, in percent (if there is one) |
| `order` | number | yes | Suggested exploring order |
| `status` | enum | yes | `draft` \| `published` |

Body: the world's story and setting, for students.

### 5.4 Game: `src/content/games/<slug>/index.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `world` | world ref | yes | |
| `summary` | string | yes | One sentence |
| `concepts` | concept refs | yes | At least one. Topics are derived from these |
| `game_type` | enum | yes | `card` \| `board` \| `role-play` \| `puzzle` \| `other` |
| `players` | {min, max} | yes | Per game copy |
| `grouping` | enum list | yes | `pairs` \| `small-groups` \| `whole-class` |
| `minutes` | {min, max} | yes | Typical play time |
| `prep_minutes` | number | yes | Teacher prep |
| `grade_bands` | enum list | yes | `6-8` \| `9-12` |
| `materials` | string list | yes | Beyond the printables, e.g., "1 die per group" |
| `printables` | printable list | yes | See 5.5. At least one |
| `variants` | variant list | no | See 5.6 |
| `standards` | standard refs | no | |
| `media` | list | no | Images or a short rules video, with captions |
| `status` | enum | yes | `draft` \| `published` |
| `credits` | string | no | Co-designers, sources, adaptations |
| `license` | string | no | Defaults to CC BY-NC-SA 4.0 |

Two body files:

- `index.md` (student-facing): `## The story`, `## How to play`, `## Winning`, `## After you play`
- `guide.md` (educator-facing): `## Overview`, `## Setup`, `## Running the game`, `## Debrief`,
  `## Assessment`, `## Differentiation`

### 5.5 Printable (inside a game's front matter)

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | E.g., "Card deck" |
| `file` | path | yes | PDF in the game's `printables/` folder |
| `paper` | enum | yes | `letter` \| `a4` \| `both` |
| `color` | enum | yes | `color` \| `bw` \| `both` |
| `copies` | string | yes | E.g., "1 per group" |
| `source` | path | no | Editable source file, for teachers who adapt it |

### 5.6 Variant (inside a game's front matter)

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `summary` | string | yes | What changes |
| `concepts` | concept refs | no | Extra concepts this variant brings in |
| `grade_bands` | enum list | no | If different from the game |

### 5.7 Pathway: `src/content/pathways/<slug>.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `summary` | string | yes | |
| `grade_bands` | enum list | yes | |
| `steps` | list of {game, variant?, note?} | yes | In order |
| `status` | enum | yes | |

### 5.8 Standard: `src/content/standards/<framework>.yaml`

A list of `{code, text, grade_band}` entries, one file per framework (e.g., `csta.yaml`).

### 5.9 Example game file

```yaml
---
name: Example Card Game
world: example-world
summary: One sentence on what players do.
concepts: [training-data, classification]
game_type: card
players: { min: 2, max: 4 }
grouping: [small-groups]
minutes: { min: 20, max: 35 }
prep_minutes: 10
grade_bands: [6-8, 9-12]
materials: ["1 die per group"]
printables:
  - { title: Card deck, file: printables/deck.pdf, paper: both, color: both, copies: 1 per group }
  - { title: Rules sheet, file: printables/rules.pdf, paper: both, color: bw, copies: 1 per group }
status: draft
---
```

### 5.10 Build-time checks

The build fails if:

- a reference (world, concept, topic, standard, game) points to something that does not exist
- a required field is missing or a value is outside its enum
- a listed printable file is missing
- there are not exactly six topics
- a published game is in a draft world, or uses a draft concept

The build warns if:

- a published game has no printables yet
- a concept is taught by no published game
- a published game has no `guide.md`
- an image has no alt text

Derived data, computed at build time and never written by hand:

- a game's topics (from its concepts)
- a concept's games (reverse links)
- "Next in this concept" links between games that share concepts

## 6. Site structure

### 6.1 URLs

| URL | Page | Main audience |
|---|---|---|
| `/` | Home: the world map, with a clear path to the educator area | Both |
| `/worlds/` | All worlds | Students |
| `/worlds/<world>/` | World page | Students |
| `/games/<game>/` | Game page: story and how to play | Students |
| `/concepts/` | All concepts, grouped by topic, with a concept map | Both |
| `/concepts/<concept>/` | Concept page | Both |
| `/topics/<topic>/` | Topic page: its concepts and games | Both |
| `/educators/` | Educator home: catalog with filters | Educators |
| `/educators/games/<game>/` | Educator guide, printables, standards | Educators |
| `/educators/pathways/` | All pathways | Educators |
| `/educators/pathways/<pathway>/` | Pathway page | Educators |
| `/search/` | Search across everything | Both |
| `/log/` | My quest log (browser storage only) | Students |
| `/about/` | About, license, credits | Both |

Games have flat URLs (`/games/<game>/`) so a game keeps its URL even if it moves to another world.

### 6.2 Page contents

**World page:** art, story, the world's games as cards, the concepts found in this world, and
links to neighboring worlds.

**Game page (student):** summary, story, how to play (text, images, optional video), winning,
"after you play" questions, the concepts it teaches (each linking to its concept page), a
printable rules sheet, and a link to the educator guide.

**Educator guide:** a facts panel (players, time, prep, grades, materials), printables with
download buttons, setup, running the game, debrief, assessment, differentiation, variants,
standards, and "pairs well with" games that share concepts.

**Concept page:** student summary and "What's really going on" first, then a collapsible
educator section (background, misconceptions), the games that teach it, and related concepts.

**Topic page:** introduction, its concepts, and its games.

**Educator catalog:** filterable list of published games. Filters: topic, concept, grade band,
time, players, grouping, game type, prep time, and standard. Filters are reflected in the URL so a
filtered view can be shared.

### 6.3 Navigation

- Header on every page: Worlds, Concepts, Educators, Search, and the quest log.
- Breadcrumbs on world, game, concept, and educator pages.
- Every game page links to its world, its concepts, and its educator guide.
- Every educator page links back to the student page it describes.

### 6.4 Two views

The student and educator views are separate pages over the same content, not a toggle that hides
content. This keeps student pages short and readable, and lets educator pages be dense. Educator
pages are not secret; anyone may read them.

## 7. Features

### 7.1 World map

An illustrated map of the worlds on the home page, with each world as a link. It must have a
text alternative: the same worlds as an ordered list, visible to screen readers and on small
screens. Whether the map is illustrated, pixel art, or something else is **(open)**.

### 7.2 Concept map

A diagram of concepts grouped by topic, with lines between related concepts and between
concepts that share games. It is generated from the content, never drawn by hand. It also has a
text alternative (the grouped list).

### 7.3 Search

Full-text search across worlds, games, concepts, and guides, built as a static index at build
time (Pagefind). No search queries leave the browser.

### 7.4 Quest log

An optional log of a student's journey: worlds visited, games played (marked by the student),
and concepts explored. It is stored only in that browser (`localStorage`), and works without it.

- Nothing is sent anywhere, and there is no way to identify a student.
- A "clear my log" button is always visible.
- A printable quest log offers the same thing on paper, for classrooms without devices.

Storage key and shape:

```json
{ "csworlds.log.v1": { "visited": ["world-slug"], "played": ["game-slug"], "concepts": ["concept-slug"] } }
```

### 7.5 Print packs

Each game offers its printables one by one, and as one combined "print pack" PDF per paper size,
built at build time. Each printable shows paper size, color or black and white, and copies needed.

### 7.6 Sharing

Every game and concept page has a short URL and a printable QR code, so a teacher can put it on a
card, a slide, or the board.

## 8. Technical design

| Need | Choice | Notes |
|---|---|---|
| Site generator | **Astro**, static output | Content collections give the typed schemas and reference checks in section 5 |
| Hosting | **GitHub Pages**, deployed by GitHub Actions | Builds on every push to `main`; not turned on until launch |
| Search | **Pagefind** | Static index; no server |
| Catalog filters | A JSON index built at build time, filtered in the browser | Small enough to load at once |
| Print packs | PDFs merged at build time (e.g., with `pdf-lib`) | |
| Diagrams | Generated SVG from the content | Concept map, world links |
| Styles | Plain CSS with design tokens | Light and dark color schemes; print styles for every page |
| Scripts | Minimal, progressive enhancement | Every page's core content works without JavaScript |

### 8.1 Repository layout

```
src/
  content/
    topics/  concepts/  worlds/  games/  pathways/  standards/
  content.config.ts      Schemas and reference rules (section 5)
  pages/                 One template per page type (section 6)
  components/            Shared pieces: cards, facts panel, filters, map
  styles/
public/                  Static files copied as they are
scripts/                 Build helpers: print packs, QR codes, checks
docs/                    This spec and other planning docs
.github/workflows/       Build and (later) deploy
```

### 8.2 Performance and compatibility

- Each page under 200 KB of HTML, CSS, and JavaScript, not counting images.
- Images served in modern formats at sensible sizes, with width and height set.
- Works on current Chrome, Edge, Safari, and Firefox, including school Chromebooks and iPads,
  and at 320 px wide.

### 8.3 Accessibility

- WCAG 2.2 AA.
- Keyboard access everywhere, with visible focus.
- Every diagram and map has a text alternative.
- Student pages written at about a grade 6 reading level.
- Rules videos have captions and a text version.
- Printables are tagged PDFs where possible, with a large-print version for text-heavy sheets.

### 8.4 Privacy

- No accounts, cookies, analytics, fonts, or scripts from third parties.
- No forms that collect personal data.
- The quest log never leaves the browser.
- This is designed to keep the site clear of COPPA and FERPA concerns. Confirm with your district
  or a privacy reviewer before launch.

## 9. Adding content

1. Copy a template from `templates/` (to be created in phase 1) into the right content folder.
2. Fill in the front matter and body sections.
3. Put printables in the game's `printables/` folder.
4. Run the site locally and fix anything the build checks report.
5. Set `status: published` when it is ready.

A new game needs no code changes: the world page, concept pages, catalog, search, and print pack
all update from its file.

## 10. Phases

| Phase | Scope | Done when |
|---|---|---|
| **1. Content model** | Write the schemas and templates; enter the two existing card games, their worlds, and their concepts | The build passes with both games, and the model needed no workaround to fit them |
| **2. Core pages** | World, game, educator guide, concept, and topic pages; header and navigation | A student can go from the home page to a game's rules, and an educator to its printables, in three clicks or fewer |
| **3. Ways in** | World map, concept map, search, educator catalog with filters | Every published game can be found through each of them |
| **4. Extras** | Quest log, print packs, QR codes, pathways | One pathway is published using both games |
| **5. Launch** | Accessibility and privacy review, GitHub Pages deploy | The review finds no open issues; the site is live |

After launch, worlds and games are added without changing the system.

## 11. Open decisions

| # | Decision | Affects |
|---|---|---|
| 1 | The two existing card games: names, worlds, and the concepts each teaches | Phase 1 |
| 2 | Can students use the site on their own, or mainly through a teacher? | How much the student view must stand alone; reading level; quest log |
| 3 | One game per world, or several from the start? | World pages; map |
| 4 | Visual identity: illustrated map, pixel art (as in the archive), or something else | World map, art, design tokens |
| 5 | Standards frameworks beyond CSTA (e.g., AI4K12, state standards) | Standards files; catalog filter |
| 6 | Printable source format to keep in the repo (e.g., InDesign, Google Docs, Word) | Printables |
| 7 | Rules videos: host where, if at all? (No third-party embeds under the privacy rules) | Game pages; file sizes |
| 8 | Custom domain, or `mrenne.github.io/csworlds` | Deploy |
| 9 | License for the site's code (e.g., MIT), separate from the CC content license | Repo |
