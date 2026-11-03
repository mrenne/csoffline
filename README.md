# Computation Quests

**Computation Quests** is a free educational ecosystem for middle and high school teachers
teaching computer science, data science, computational thinking, cybersecurity, and AI literacy.

Computation Quests is one map, a continent divided into regions. Each region is a subject area with lessons,
activities, and resources for teachers, plus activities students use directly in the browser.

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

- **Free.** Every lesson, activity, and resource is free to use.
- **No student accounts.** Student activities run anonymously in the browser and collect no
  personal data.
- **Teacher-friendly.** Lessons are written so a teacher new to the topic can teach them.
- **Openly licensed.** Content is shared under CC BY-NC-SA 4.0 so teachers can adapt and remix it.

## Repository layout

```
map/                  The Computation Quests map: generator, image, and viewer page
areas/                One folder per region, named by subject
  data-science/
    map/              The Data Science region map
    lessons/          Teacher-facing lessons
    activities/       Student-facing interactive activities
    unplugged/        No-device activities
    resources/        External links, repos, readings, datasets
docs/                 Project planning: vision, roadmap, decisions, area template
templates/            Copy-and-fill templates for lessons, activities, and resources
inbox/                Drop zone for existing materials before they are sorted into a region
```

## Where to start

- [Computation Quests map](map/index.html) (see [map/README.md](map/README.md) to build and view it)
- [Vision](docs/vision.md): who this is for and what it is
- [Roadmap](docs/roadmap.md): phased plan
- [Area template](docs/area-template.md): the structure every region follows
- [Decisions](docs/decisions.md): decisions made so far and open questions

## License

Unless otherwise noted, all content in this repository is licensed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)
(CC BY-NC-SA 4.0). See [LICENSE](LICENSE).

The map tile art comes from the La Petite Tile Maps pack and is **not** covered by this license
or included in the repository. See [map/README.md](map/README.md).

To attribute, use something like:

> "Lesson Title" from Computation Quests by Mike Renne, licensed under CC BY-NC-SA 4.0.
> https://github.com/mrenne/csworlds
