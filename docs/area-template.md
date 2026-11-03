# Area template

Every region uses the same structure so teachers can find their way around any of them.

## Folder layout

Folders are named by subject, not display name, so they stay stable if names change.

```
areas/<subject>/
  README.md        Area overview (sections below)
  map/             The region's own map (optional)
  lessons/         One folder per lesson, from templates/lesson-template.md
  activities/      Student-facing interactive activities, from templates/activity-template.md
  unplugged/       No-device activities (same lesson template, marked unplugged)
  resources/       links.md: external links, GitHub repos, datasets, readings
```

## Area README sections

| Section | Purpose |
|---|---|
| Overview | What the region covers, in two or three sentences |
| Places | The named places on the region map and the concept each one stands for |
| Big ideas | 3–5 core concepts, written for teachers |
| Learning progression | What fits middle school vs. high school |
| Lessons | Table of lessons with grade band, duration, and plugged/unplugged |
| Student activities | List of interactive activities |
| Teacher primer | A 10-minute content introduction for teachers new to the topic |
| Common misconceptions | What students (and adults) often get wrong |
| Standards | Standards this region addresses |
| Resources | Link to `resources/links.md` |

## Human-in-the-loop (author note)

Design each activity so the student's own judgment is needed to finish it: a decision the program
cannot make, an output that must be checked, a choice behind the data. Do not label this for
students; let them notice it. See [vision](vision.md).

## Metadata

Each lesson and activity starts with a YAML front matter block (see `templates/`). That metadata
will drive the website's search and filters later, so fill it in carefully.
