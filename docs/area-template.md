# Area template

Every region uses the same structure so teachers can find their way around any of them. All
content is unplugged: students use no technology (see [vision](vision.md)).

## Folder layout

Folders are named by subject, not display name, so they stay stable if names change.

```
areas/<subject>/
  README.md                Area overview (sections below)
  extra.html               Optional hand-written section for the region's web page
  map/                     The region's own map (optional)
  activities/
    <activity-slug>/
      README.md            Teacher guide, from templates/activity-template.md
      printables/          Print-ready handouts (PDF), plus editable sources
  resources/               links.md: teacher background reading and related collections
```

The **activity** is the unit of content. A lesson is one or more activities in a class period; an
activity's guide includes the full period plan, so there is no separate lesson document.

## Area README sections

| Section | Purpose |
|---|---|
| Overview | What the region covers, in two or three sentences |
| Places | The named places on the region map and the concept each one stands for |
| Big ideas | 3–5 core concepts, written for teachers |
| Learning progression | What fits middle school vs. high school |
| Activities | Table of activities: topic, grade band, duration, group size, status |
| Activity ideas | Unplugged ideas not yet written up, by topic |
| Teacher primer | A 10-minute content introduction for teachers new to the topic |
| Common misconceptions | What students (and adults) often get wrong |
| Standards | Standards this region supports, noting any that also need a computer |
| Resources | Link to `resources/links.md` |

## Human-in-the-loop (author note)

Design each activity so the student's own judgment is needed to finish it: a case the algorithm
cannot decide, an output that must be checked, a choice behind the data. Do not label this for
students; let them notice it. See [vision](vision.md).

## Metadata

Each activity starts with a YAML front matter block (see `templates/activity-template.md`). That
metadata will drive the website's search and filters later, so fill it in carefully.
