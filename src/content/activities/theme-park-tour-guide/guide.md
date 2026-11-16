---
---

## Overview

Students plan a tour of a theme park that visits every ride exactly once and returns to the start.
Along the way they turn a detailed map into a graph (abstraction), write and trace a route (an
algorithm for one problem), prove that a map has no tour, and write general rules that find a tour on
any map. Computer scientists call this kind of tour a Hamiltonian cycle.

## Learning objectives

- Represent a problem as a graph of nodes and edges, leaving out details that don't matter.
- Write a solution as a precise sequence of steps.
- Trace an algorithm against a set of requirements to find bugs.
- Explain why a problem has no solution.
- Tell the difference between a solution to one problem and an algorithm for a whole class of problems.

## Pacing

| Part | Pages | Time |
| --- | --- | --- |
| Part 1: Draw the graph, plan a tour, trace with a partner | 1–3 | 15 minutes |
| Part 2: Map B, the full park | 4 | 8 minutes |
| Part 3: Map C, the Sky Ride | 5 | 7 minutes |
| Part 4: Write tour-finding rules and test them on Map D | 6–7 | 12 minutes |
| Discussion | — | 5 minutes |
| Extra: Debug the tour | 8 | 10 minutes |

Debug the tour works well as a warm-up the next day or as an exit ticket. Hand it out after students
have checked their Part 1 graph, because it shows the Lakeside Park graph.

## The maps

| Map | Rides | Tours | What it teaches |
| --- | --- | --- | --- |
| Lakeside Park (Part 1) | 7 + gate | 3 | Abstraction: the same 12 connections as a busy park map |
| Map B | 11 + gate | 1 | Forced moves: the Arcade and Mini Golf have only two paths |
| Map C | 10 + gate | 0 | Proof: the Sky Ride is the only way between the two sides |
| Map D | 9 + gate | 1 | Testing rules on a map students haven't seen |

## Tips

- Students' Part 1 graphs won't look like the answer key, and that's fine. A graph is correct when
  it has the same connections. Comparing two different-looking drawings that have the same
  connections is a good discussion.
- The picnic tables are on a dead-end path. Students who draw them as a node have found a good
  question: does the tour need to go there?
- When tracing, the tracer should follow the steps exactly as written, even when the writer
  obviously meant something else. That's what a computer does.
- On Map C, push past "I tried and it didn't work." The goal is an argument that would convince
  someone who hasn't tried at all.
- In Part 4, students who reach Map D and still have to guess have found a gap in their rules.
  Undoing a guess and trying another path (backtracking) is a real algorithm step, not cheating.

## Key vocabulary

| Term | Meaning |
| --- | --- |
| Graph | A set of nodes joined by edges |
| Node | A dot in a graph; here, a ride or the Front Gate |
| Edge | A line between two nodes; here, a path between two rides |
| Abstraction | Leaving out details that don't matter to the problem |
| Algorithm | Steps that solve every problem of a certain kind |
| Requirement | Something a correct solution must do |
| Trace | Following an algorithm step by step on paper to check it |

## Going further

- Add walking times to the paths and look for the fastest tour. This is the traveling salesperson
  problem, and no one knows a fast way to solve it for big maps.
- Ask for a route that walks every path exactly once instead of visiting every ride, the way a
  snowplow or mail carrier would. That's an Euler circuit, and there's a quick test for whether
  one exists.
- Have students draw a graph of their school and plan a tour for new students.

## Credits

This activity is a remix of *Tour Guide* (V1.1, 2014) by Paul Curzon, Queen Mary University of
London, for [Teaching London Computing](http://teachinglondoncomputing.org), used under CC BY-NC-SA.
The remix adds a new theme park setting and maps, a draw-the-graph map, a map with no tour, a
rule-writing challenge, peer tracing, and a debugging page.
