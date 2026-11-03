# World template

Every World uses the same structure so teachers can find their way around any World.

## Folder layout

```
worlds/<world-name>/
  README.md        World overview (sections below)
  lessons/         One folder per lesson, from templates/lesson-template.md
  activities/      Student-facing interactive activities, from templates/activity-template.md
  unplugged/       No-device activities (same lesson template, marked unplugged)
  resources/       links.md: external links, GitHub repos, datasets, readings
```

## World README sections

| Section | Purpose |
|---|---|
| Overview | What this World covers, in two or three sentences |
| Big ideas | 3–5 core concepts, written for teachers |
| Learning progression | What fits middle school vs. high school |
| Lessons | Table of lessons with grade band, duration, and plugged/unplugged |
| Student activities | List of interactive activities |
| Teacher primer | A 10-minute content introduction for teachers new to the topic |
| Common misconceptions | What students (and adults) often get wrong |
| Standards | Standards this World addresses |
| Resources | Link to `resources/links.md` |

## Metadata

Each lesson and activity starts with a YAML front matter block (see `templates/`). That metadata
will drive the website's search and filters later, so fill it in carefully.
