---
name: Model Cards
domains: [ethics, ai-literacy]
student_summary: Every AI model has strengths and limits. A model card tells you what they are, and what it leaves out.
related: [training-data, bias, responsible-ai-use]
---

## What's really going on

A machine learning model only knows what it learned from its training data, so it works well in
some situations and badly in others. A **model card** is a short fact sheet that describes a model:
what it's for, what data it was trained on, how well it did in tests, who it might not work well
for, and what to watch out for. Reading one, and checking it against how the tool actually
behaves, is how you decide whether an AI tool is right for a job.

## Background

Model cards were proposed in 2019 by a team of researchers led by Margaret Mitchell, as a standard
way to report how a model was built and tested. Many AI companies and model-sharing sites now
publish them. A good model card reports results for different groups of people, not just one
overall score, because a model can be 97% accurate overall and much less accurate for some people.
Related documents include **datasheets for datasets**, which describe where training data came
from, and **system cards**, which describe a whole AI product.

Model cards are written by the people who made the model, so they can leave things out. That's
why independent testing matters: researchers, journalists and users often discover limitations
the maker didn't report.

## Misconceptions

- An accuracy score tells you how well a model works for everyone. A single score can hide big
  differences between groups, situations or kinds of input.
- If a model card doesn't mention a problem, there isn't one. Some limitations haven't been tested
  for, and some aren't reported.
- The most accurate tool is always the best choice. Privacy, fairness, energy use and the job
  itself matter too, and sometimes the best choice is no AI at all.
- Limitations are bugs that will be fixed in the next version. Many limitations come from the
  training data, and only change when the data changes.
