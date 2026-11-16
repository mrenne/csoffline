---
name: Correlation and Causation
domains: [data-science]
student_summary: Telling the difference between two things that happen together and one thing that makes the other happen.
related: [sampling]
---

## What's really going on

Two things are correlated when they tend to change together. Ice cream sales and sunburns both rise in summer, but ice cream doesn't cause sunburns: hot, sunny weather causes both. Causation means one thing actually makes the other happen, and showing that usually takes a careful test where you change only one thing. Data scientists are always asking whether a pattern in the data is a real cause or just a coincidence.

## Background

A correlation is a statistical relationship between two variables; causation means changing one actually changes the other. Correlations can come from a hidden third variable (a confounder), from reverse causation, or from pure coincidence, especially when many variables are compared. Randomized controlled experiments are the standard way to test causation, because random assignment balances out other factors. Students meet misleading causal claims constantly in ads, headlines, and social media, so this idea transfers well beyond CS.

## Misconceptions

- A strong correlation proves causation. Even a very strong relationship can be driven by a confounder or by chance.
- No correlation means no connection at all. A relationship can be real but non-linear, or masked by other factors.
- If A comes before B, A caused B. Timing alone doesn't rule out coincidence or a shared cause.
