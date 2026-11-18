---
---

## Overview

Talent Stack is a series of card games about tech careers. In the Data Science Edition, teams act as
hiring managers and draft a three-person team from 12 data science career cards to complete a
Project Quest on a budget. During the draft they see only each card's job title, salary tier, and
tech skills. At the audit they flip the cards to find the real salaries, minimum degrees, and job
duties, so students' assumptions about these careers get tested against the facts.

The edition is a prototype. The core rules have been playtested. The Market Event cards, the Secret
Company cards, and quests 4–12 have not been playtested yet.

## The deck

| Cards | Count | What they do |
| --- | --- | --- |
| Career | 12 | Data Analyst, Machine Learning Engineer, Data Engineer, Chief Data Officer, AI Research Scientist, Cybersecurity Data Analyst, Bioinformatics Specialist, Sports Analytics Specialist, Game Data Analyst, Climate Data Scientist, Social Media Data Analyst, Healthcare Data Scientist |
| Project Quest | 12 | A mission, three required roles, and a budget cap. Every career is required by exactly 3 quests. |
| Market Event | 12 | One is drawn face-up each game and changes salaries, budgets, or scoring for everyone. |
| Secret Company | 8 | Each team draws one in secret. It pays a bonus of up to +2 at the end. |

The tech stack icons on the card fronts are SQL, Python, Tableau, Cloud, and Security.

## Setup

- Print the card deck two-sided on cardstock, flipping on the long edge, at 100% scale. Then cut out
  the cards. One deck serves one table.
- Print one rules sheet per table.
- Use 2 or 3 teams per deck, so there are always cards left in the pool for the trade. At a table of
  2–3 students, each student is a team. At a table of 4–6, students pair up.

## Running the activity

| Phase | Time |
| --- | --- |
| Setup | 0:00–3:00 |
| Blind draft and audit | 3:00–8:00 |
| Fast trade and re-audit | 8:00–13:00 |
| Team pitches | 13:00–17:00 |
| Debrief | 17:00–20:00 |

### Audit scoring

| Category | Points | Rule |
| --- | --- | --- |
| Role match | +5 each | Each card that matches a required role on the Quest. |
| Stand-in | +1 each | A missing role is covered by another card that shares a tech icon with it. One role per card. |
| Budget | +3 | Total salary at or under the cap. Over the cap, lose 1 point per $10,000 over (round up). |
| Synergy | +1 or +3 | The team's most-shared tech icon is on 2 cards (+1) or all 3 (+3). |

The highest possible audit score is 19.

### Trade abilities

The retro icon on the back of each career card gives it an ability during the trade. The icons never
score points.

| Icon | Ability |
| --- | --- |
| Rotary phone | **Call Out:** trade this card for any card on another team instead of the pool. |
| Floppy disk | **Save:** no other team can Call Out this card. |
| VHS tape | **Rewind:** if your re-audit score drops, undo your pool trade. |
| CRT computer | **Preview:** before trading, peek at the backs of 2 pool cards. |

### Pitch

You judge each team's 30-second pitch and award 1 point for each of these:

- It names a real job duty from the back of every card.
- It explains why the team fits the quest.
- It finishes within 30 seconds.

## Debrief

- Which job surprised you most when you flipped it?
- Was the most expensive role worth it?
- What schooling would your dream job need?

## Assessment

The pitch is a quick check on whether students read and understood the job duties on the backs of
the cards. The audit is also a chance to check students' addition with large numbers.

## Differentiation

- For a first game, draw the Steady Market card, which changes nothing, and leave out the Company
  cards. Add them in later games.
- Pair students up so that one partner can focus on the budget math while the other reads the job
  duties.

## Before you print

The salaries on the cards are placeholders from the original design document, and each card back
says "salary unverified." They should be checked against a cited, dated source, such as the BLS
Occupational Outlook Handbook, before final printing. The source files, design notes, and balance
check script are in the [GitHub repository](https://github.com/mrenne/talent_stack_card_game).
