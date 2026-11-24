---
---

## Overview

Data Defenders asks students to examine scenarios involving sensitive information, classify the
data in each one, choose security measures, and explain how each measure protects confidentiality.
To make that work for middle school, it's built as a game with five extra pieces:

- **School case files.** Eight scenarios students know from their own school, like the nurse's
  office, lunch accounts, the yearbook, and smartwatches on the cross-country team. Each one has
  risks planted in it for students to spot.
- **A budget.** Sensitivity sets the budget: 5 shields for private data, 8 for highly sensitive.
  Defenses cost 1 or 2 shields, so students can't buy everything and have to make trade-offs.
- **Defense cards with trade-offs.** Twelve security measures, each with what it does and what it
  costs the people who use the data. One card, Backup copy, protects availability but not
  confidentiality. It's a deliberate trap.
- **A red team.** Groups attack each other's plans with twelve threat cards, from a password
  guesser to a fake caller. A defense only counts if students can explain how it stops the threat.
- **Breach reports.** When a threat gets through, students write what leaked and who it could harm.
  This turns a lost point into the most useful writing of the lesson.

## The case files

| Case | Data | Level | The point of the case |
| --- | --- | --- | --- |
| 1. The Nurse's Office | Personal, health | Highly sensitive | Share only what each person needs |
| 2. Lunch Accounts | Personal, money, login | Highly sensitive | Shoulder surfing, and not storing card numbers |
| 3. Mr. Okafor's Gradebook | Personal, school record | Private | A small budget forces choices |
| 4. The Counselor's Notebook | Personal, health | Highly sensitive | Paper only: computer defenses do nothing |
| 5. Field Trip Forms | Personal, health, location | Highly sensitive | Collect less, and split up what you carry |
| 6. The Club Store | Personal, money, location, login | Highly sensitive | A shared password |
| 7. The Yearbook | Personal | Highly sensitive | Mixed data: public names, but a sensitive list |
| 8. Cross-Country Watches | Personal, health, location | Highly sensitive | Location data reveals where kids live |

Page 8 of the printable has a strong plan for each case and the risks planted in each one.

## Preparing

- Print pages 5 and 6 on card stock if you can, and cut a set of defense and threat cards for each
  group. Envelopes keep them together.
- Choose case files. Give each group one case file, or two if you have 90 minutes. Two groups with
  the same case make a good comparison later. Case 4 and case 7 are the trickiest; give them to
  groups who like a puzzle.
- Decide who plays red team: another group (more engaging) or you (faster and easier to manage).

## Running the activity

**Session 1 (45 minutes): classify and defend**

1. **Hook (5 minutes).** Ask: "What's something the school knows about you that you wouldn't want
   posted on the wall?" Collect answers without names, then sort them on the board into what's
   public, private and highly sensitive.
2. **Model it (10 minutes).** Walk through the library example on page 2, then introduce the CIA
   triad on page 1. Point out that this activity is about the C.
3. **Classify (10 minutes).** Groups read their case file, fill in Spot the risks, and complete step
   1 of the plan sheet. Ask: "What's the worst thing that could happen if this got out?"
4. **Plan (20 minutes).** Groups spend their shields and write a "how it protects" sentence for
   each defense. Circulate and push for specifics: "Who does that stop, and how?"

**Session 2 (45 minutes): attack and debrief**

1. **Attack round (25 minutes).** Pair up groups. Deal each red team 6 threat cards; they play the
   3 they think will get through. Score each threat as blocked, spotted or a breach, then switch.
2. **Breach reports (10 minutes).** Every group with a breach writes a report. Groups with no
   breaches write about the threat they were most worried about.
3. **Debrief (10 minutes).** Use the questions below.

For a single 60-minute period, skip the hook, give every group the same case file, and have
you play red team for the whole class at once.

## Things to watch for

- **"Encryption fixes everything."** Encryption protects a lost device and data on Wi-Fi, but it
  doesn't stop a curious insider who's allowed to log in, or a fake caller. Ask: "Does this person
  already have the key?"
- **Buying the backup.** Backups keep data from being lost, not from being seen. If students buy it,
  don't take the shield back: ask which threat it stops, and let them find out it doesn't stop any.
- **Computer defenses for paper.** In case 4, two-step login and encryption do nothing. A plan that
  spends only 4 of 8 shields is stronger than one that spends all 8 on the wrong things.
- **Vague explanations.** "It makes it more secure" isn't an explanation. The sentence frame on the
  plan sheet helps: "Two-step login stops a hacker with a stolen password from logging in, because
  they don't have the code on the nurse's phone."
- **Real data.** If students bring up real incidents at your school, steer back to the made-up case
  files. Nobody should share real details about classmates.

## Debrief

- Which kind of data did your group treat as most sensitive? Why?
- Which defense stopped the most threats across the class? Which threat was hardest to stop?
- When was collecting less better than any defense you could buy?
- Which defense has the biggest trade-off for the people who use the data? When is it worth it?
- What does the Backup copy card protect, if not confidentiality?

## Differentiation

- **Grades 6–8:** play as written. For more support, give groups case 3 first, which has the
  smallest budget and the most familiar data.
- **Grades 9–12:** add a trade-off for every defense on the plan sheet, as in standard
  HS-SYS-SE-31, and have students argue whether each one is worth its cost. Groups can also
  research which laws cover each case (FERPA, HIPAA, COPPA) and add a column for them.

## Going further

- **Design a case file.** Have groups write a new case file about a place they know, like a doctor's
  office, a gym or a game app, with three risks planted in it. Swap with another group.
- **New threats.** Have students design a threat card that none of the defenses stop, then design
  the defense that would.
- **Integrity and availability.** Play again with the I and A of the CIA triad: a threat that changes
  grades, or one that locks the lunch system on a busy day. The Backup copy card finally earns its
  shield.
- [The CSTA PK–12 Computer Science Standards](https://csteachers.org/pk12standards/) (MS-SYS-SE-32,
  HS-SYS-SE-31) describe the CIA triad and the trade-offs of security measures.
