# CS Offline system spec

> Status: **draft**, November 2026. Phase 2 core pages are built in Astro with placeholder content. This spec covers the system: the content model, the website,
> and how content is added. It does not cover the activities or curriculum themselves, which are
> designed separately. Items marked **(open)** need a decision; see [Open decisions](#open-decisions).

## 1. Purpose

CS Offline gives teachers and students resources to teach and learn computer science without
lots of technology. The website is where people find unplugged activities and resources, learn how
they work, get the printables, and explore the ideas behind them. Some activities are games, such
as card games or trading card games; others are not. None needs technology to run.

The system is organized into six **learning domains**: Computer Science, Computational Thinking,
Data Science, AI Literacy, Cybersecurity, and Ethics. Every activity has one home domain. Activities are
also connected by the **ideas** they teach, and each idea belongs to one or more domains.
That web of links is what makes a set of separate activities into one system.

The levels read as one ladder: a **domain** says what subject it is, an **idea** says exactly what
it teaches, and an **activity** says what people do.

## 2. Principles

1. **Activities are always unplugged.** No activity may require the website or any device to run.
   The site supports the activities; it is never part of the activity itself.
2. **No accounts, no student data.** No sign-in, no cookies, no analytics, no third-party
   requests. Anything personal, such as progress, stays in the visitor's own browser.
3. **Licensed per activity.** Nothing is assumed to be Creative Commons; an activity states its
   license when it has one.
4. **Content, not pages.** Every page is generated from structured content files. Adding an activity
   means adding files, not building pages.
5. **Structure is checked.** The content model is enforced at build time; broken links between
   content fail the build instead of reaching the site.
6. **One content set, two views.** Students and educators see the same domains, activities,
   and ideas, presented for their needs.
7. **Accessible and fast.** WCAG 2.2 AA, usable on a phone or a school Chromebook, and readable on
   a classroom projector.

## 3. Users

| User | Goals | Typical entry point |
|---|---|---|
| **Student** (grades 6–12) | Find a domain, learn an activity's rules, understand "what's really going on" | The home page, or a link or QR code from a teacher or a printed card |
| **Educator** | Find an activity for a domain or idea, prepare and print it, run and debrief it, plan a unit | The catalog, a domain or idea page, search |
| **Author** (the project team) | Add and update activities, ideas, and printables | The content files in the repo |

Whether students use the site on their own or mainly through a teacher is **(open)**. The spec
assumes the student view must stand on its own.

## 4. Core terms

```
Domain 1──* Activity        (each activity has one home domain)
Domain *──* Idea *──* Activity
                          │
                          ├──* Printable
                          ├──* Variant
                          └──* Standard
Pathway *──* Activity   (an ordered list)
```

| Term | Meaning |
|---|---|
| **Learning domain** | One of six fixed areas: Computer Science, Computational Thinking, Data Science, AI Literacy, Cybersecurity, Ethics |
| **Idea** | A specific thing an activity teaches, such as training data, sampling, or encryption. Belongs to one or more domains |
| **Activity** | An unplugged learning activity. Some are games (card game, trading card game, board game); others are role-plays, puzzles, simulations, or discussions. Has one home domain |
| **Variant** | A named change to an activity's rules, often to focus on a different idea or grade band |
| **Printable** | A file to print for an activity: cards, boards, rules, log sheets |
| **Pathway** | An ordered sequence of activities for a unit or course, written for educators |
| **Standard** | A standards statement, such as a CSTA code, that an activity supports |

An activity's home domain is where it is listed first. It also appears under every other domain its
ideas belong to, as an activity that "also teaches" that domain.

## 5. Content model

Content lives in files under `src/content/`, as Markdown with YAML front matter. The body of each
file is free text; the front matter is checked against the schema below. Slugs come from file or
folder names and never change once published (they are the URLs).

### 5.1 Learning domain: `src/content/domains/<slug>.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Display name |
| `summary` | string | yes | One sentence |
| `color` | string | yes | Design token name, not a hex value |
| `icon` | string | yes | Icon name from the site's icon set |
| `order` | number | yes | Display order |

Body: a short introduction. Exactly six domain files exist; adding a seventh fails the build.

### 5.2 Idea: `src/content/ideas/<slug>.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `domains` | domain refs | yes | At least one |
| `student_summary` | string | yes | One or two sentences at a grade 6 reading level |
| `related` | idea refs | no | Shown as "see also" |
| `standards` | standard refs | no | |

Body sections, by heading:

- `## What's really going on`: for students; how the idea works in real systems
- `## Background`: for educators
- `## Misconceptions`: for educators

### 5.3 Activity: `src/content/activities/<slug>/index.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `domain` | domain ref | yes | The home domain |
| `summary` | string | yes | One sentence |
| `ideas` | idea refs | yes | At least one. Other domains are derived from these |
| `activity_type` | enum | yes | `card-game` \| `trading-card-game` \| `board-game` \| `pencil-and-paper-game` \| `role-play` \| `puzzle` \| `simulation` \| `discussion` \| `other` |
| `audience` | enum | yes | `students` \| `educators` \| `both`. Decides which pages exist (see 6.4) |
| `link` | {label, url} | no | Where to get an activity hosted or sold elsewhere. With a link, printables and a guide are not expected, and the group, time, prep, and grade fields below are optional |
| `group_size` | {min, max} | yes | People per group |
| `grouping` | enum list | yes | `pairs` \| `small-groups` \| `whole-class` |
| `minutes` | {min, max} | yes | Typical class time |
| `prep_minutes` | number | yes | Teacher prep |
| `grade_bands` | enum list | yes | `6-8` \| `9-12` |
| `materials` | string list | yes | Beyond the printables, e.g., "1 die per group" |
| `printables` | printable list | yes | See 5.4. At least one |
| `variants` | variant list | no | See 5.5 |
| `standards` | standard refs | no | |
| `media` | list | no | Images or a short rules video, with captions |
| `status` | enum | yes | `draft` \| `published` |
| `author` | {name, role?, bio?, link?} | yes | Shown in the Author section on the activity's pages. `role` defaults to "author" (for example, "designer"). `link` is {label, url} |
| `credits` | string | no | Co-designers, sources, adaptations |
| `notice` | string | no | Legal or affiliation notice shown on the student and educator pages |
| `license` | string | no | Set only when the activity has a stated license; never assumed |
| `license_url` | url | no | Makes the license name a link |

Two body files:

- `index.md` (student-facing): `## What you'll do`, `## How it works`, `## Afterward`, plus any
  sections the activity needs (a game might add `## Winning`)
- `guide.md` (educator-facing): `## Overview`, `## Setup`, `## Running the activity`, `## Debrief`,
  `## Assessment`, `## Differentiation`

### 5.4 Printable (inside an activity's front matter)

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | E.g., "Card deck" |
| `file` | path | yes | PDF in the activity's `printables/` folder |
| `paper` | enum | yes | `letter` \| `a4` \| `both` |
| `color` | enum | yes | `color` \| `bw` \| `both` |
| `copies` | string | yes | E.g., "1 per group" |
| `source` | path | no | Editable source file, for teachers who adapt it |

### 5.5 Variant (inside an activity's front matter)

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `summary` | string | yes | What changes |
| `ideas` | idea refs | no | Extra ideas this variant brings in |
| `grade_bands` | enum list | no | If different from the activity |

### 5.6 Pathway: `src/content/pathways/<slug>.md`

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | |
| `summary` | string | yes | |
| `grade_bands` | enum list | yes | |
| `steps` | list of {activity, variant?, note?} | yes | In order |
| `status` | enum | yes | |

### 5.7 Standard: `src/content/standards/<framework>.yaml`

A list of `{code, text, grade_band}` entries, one file per framework (e.g., `csta.yaml`).

### 5.8 Example activity file

```yaml
---
name: Example Card Game
domain: ai-literacy
summary: One sentence on what students do.
ideas: [training-data, classification]
activity_type: card-game
audience: both
author: { name: Example Author, bio: One or two sentences. }
group_size: { min: 2, max: 4 }
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

### 5.9 Build-time checks

The build fails if:

- a reference (domain, idea, standard, activity) points to something that does not exist
- a required field is missing or a value is outside its enum
- a listed printable file is missing
- there are not exactly six domains
- a published activity uses a draft idea

The build warns if:

- a published activity has no printables yet
- an idea is taught by no published activity
- a published activity has no `guide.md`
- an image has no alt text

Derived data, computed at build time and never written by hand:

- an activity's other domains (from its ideas)
- a domain's activities, and the activities from other domains that also teach it
- an idea's activities (reverse links)
- "Next in this idea" links between activities that share ideas

## 6. Site structure

### 6.1 URLs

| URL | Page | Main audience |
|---|---|---|
| `/` | Home: the six domains, with a clear path to the educator area | Both |
| `/domains/` | All learning domains | Both |
| `/domains/<domain>/` | Domain page: its ideas and activities | Both |
| `/activities/` | All activities, grouped by domain | Both |
| `/activities/<activity>/` | Activity page: what you'll do and how it works | Students |
| `/ideas/<idea>/` | Idea page | Both |
| `/educators/` | Educator home: catalog with filters | Educators |
| `/educators/activities/<activity>/` | Educator guide, printables, standards | Educators |
| `/educators/pathways/` | All pathways | Educators |
| `/educators/pathways/<pathway>/` | Pathway page | Educators |
| `/search/` | Search across everything | Both |
| `/log/` | My quest log (browser storage only) | Students |
| `/about/` | About, license, credits | Both |

Activities have flat URLs (`/activities/<activity>/`) so an activity keeps its URL even if it moves to another domain.

### 6.2 Page contents

**Domain page:** introduction, its ideas, its activities as cards, the activities from other domains
that also teach it, and links to the other domains.

**Activity page (student):** summary, what you'll do, how it works (text, images, optional video),
"afterward" questions, the ideas it teaches (each linking to its idea page), a
printable rules sheet, and a link to the educator guide.

**Author section:** a large panel on student and educator activity pages with the author's name,
initials, bio, and link.

**Educator guide:** a facts panel (group size, time, prep, grades, materials), printables with
download buttons, setup, running the activity, debrief, assessment, differentiation, variants,
standards, and "pairs well with" activities that share ideas.

**Idea page:** student summary and "What's really going on" first, then a collapsible
educator section (background, misconceptions), the activities that teach it, and related ideas.

**Educator catalog:** filterable list of published activities. Filters: domain, idea, grade band,
time, group size, grouping, activity type, prep time, and standard. Filters are reflected in the URL so a
filtered view can be shared.

### 6.3 Navigation

- Header on every page: Domains, Activities, Educators, Search, and the quest log.
- Ideas are not in the header. They are reached from domain and activity pages, and filtered in the
  educator catalog.
- Breadcrumbs on domain, activity, idea, and educator pages.
- Every activity page links to its domain, its ideas, and its educator guide.
- Every educator page links back to the student page it describes.

### 6.4 Two views

The student and educator views are separate pages over the same content, not a toggle that hides
content. This keeps student pages short and readable, and lets educator pages be dense. Educator
pages are not secret; anyone may read them.

An activity's `audience` decides its pages. `students`: a student page, listed on `/activities/`.
`educators`: an educator page, listed in the catalog. `both`: both pages, listed in both places.
Domain and idea pages list all of them, labeled by audience.

## 7. Features

### 7.1 Domain overview

The home page and `/domains/` show the six domains as cards, each with its icon, summary, and
number of activities. Whether this later becomes an illustrated map or diagram is **(open)**.

### 7.2 Idea map

A diagram on `/domains/` of ideas grouped by domain, with lines between related ideas and between
ideas that share activities. It is generated from the content, never drawn by hand. It also has a
text alternative (the grouped list).

### 7.3 Search

Full-text search across domains, activities, ideas, and guides, built as a static index at build
time (Pagefind). No search queries leave the browser.

### 7.4 Quest log

An optional log of a student's journey: domains visited, activities done (marked by the student),
and ideas explored. It is stored only in that browser (`localStorage`), and works without it.

- Nothing is sent anywhere, and there is no way to identify a student.
- A "clear my log" button is always visible.
- A printable quest log offers the same thing on paper, for classrooms without devices.

Storage key and shape:

```json
{ "csoffline.log.v1": { "visited": ["domain-slug"], "done": ["activity-slug"], "ideas": ["idea-slug"] } }
```

### 7.5 Print packs

Each activity offers its printables one by one, and as one combined "print pack" PDF per paper size,
built at build time. Each printable shows paper size, color or black and white, and copies needed.

### 7.6 Sharing

Every activity and idea page has a short URL and a printable QR code, so a teacher can put it on a
card, a slide, or the board.

## 8. Technical design

| Need | Choice | Notes |
|---|---|---|
| Site generator | **Astro**, static output | Content collections give the typed schemas and reference checks in section 5 |
| Hosting | **GitHub Pages**, deployed by GitHub Actions | Builds on every push to `main`; not turned on until launch |
| Search | **Pagefind** | Static index; no server |
| Catalog filters | A JSON index built at build time, filtered in the browser | Small enough to load at once |
| Print packs | PDFs merged at build time (e.g., with `pdf-lib`) | |
| Diagrams | Generated SVG from the content | Idea map, domain links |
| Styles | Plain CSS with design tokens | Light and dark color schemes; print styles for every page |
| Scripts | Minimal, progressive enhancement | Every page's core content works without JavaScript |

### 8.1 Repository layout

```
src/
  content/
    domains/  ideas/  activities/  pathways/  standards/
  content.config.ts      Schemas and reference rules (section 5)
  pages/                 One template per page type (section 6)
  components/            Shared pieces: cards, facts panel, filters, icons
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
3. Put printables in the activity's `printables/` folder.
4. Run the site locally and fix anything the build checks report.
5. Set `status: published` when it is ready.

A new activity needs no code changes: the domain pages, idea pages, catalog, search, and print pack
all update from its file.

## 10. Phases

| Phase | Scope | Done when |
|---|---|---|
| **1. Content model** | Write the schemas and templates; enter the two existing games (Data Science Deck and Tokens TCG), their domains, and their ideas | The build passes with both activities, and the model needed no workaround to fit them |
| **2. Core pages** | Domain, activity, educator guide, and idea pages; header and navigation | A student can go from the home page to an activity's rules, and an educator to its printables, in three clicks or fewer |
| **3. Ways in** | Domain overview, idea map, search, educator catalog with filters | Every published activity can be found through each of them |
| **4. Extras** | Quest log, print packs, QR codes, pathways | One pathway is published using both activities |
| **5. Launch** | Accessibility and privacy review, GitHub Pages deploy | The review finds no open issues; the site is live |

After launch, activities and ideas are added without changing the system.

## 11. Open decisions

| # | Decision | Affects |
|---|---|---|
| 1 | Data Science Deck and Tokens TCG: summaries, details, and the ideas each teaches | Phase 1 |
| 2 | Can students use the site on their own, or mainly through a teacher? | How much the student view must stand alone; reading level; quest log |
| 3 | Visual identity beyond the current navy-and-orange theme: illustration, art for activities | Home page, activity pages, design tokens |
| 4 | Standards frameworks beyond CSTA (e.g., AI4K12, state standards) | Standards files; catalog filter |
| 5 | Printable source format to keep in the repo (e.g., InDesign, Google Docs, Word) | Printables |
| 6 | Rules videos: host where, if at all? (No third-party embeds under the privacy rules) | Activity pages; file sizes |
| 7 | Custom domain, or `mrenne.github.io/csoffline` | Deploy |
| 8 | License for the site's code (e.g., MIT), separate from activity licenses | Repo |
