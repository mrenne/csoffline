---
name: "Build a Brain: Coin Snap"
domain: ai-literacy
summary: "Build a working neural network out of coins on a paper board, then use it to play Coin Snap against a friend."
ideas: [neural-networks, loops]
activity_type: simulation
audience: both
author:
  name: Peter McOwan and Paul Curzon
  role: authors
  bio: "Peter McOwan and Paul Curzon of Queen Mary University of London created cs4fn (Computer Science for Fun) and Teaching London Computing, which share free computer science activities for students and teachers."
  link: { label: "Visit cs4fn", url: "https://www.cs4fn.org/" }
group_size: { min: 1, max: 3 }
grouping: [pairs, small-groups]
minutes: { min: 15, max: 20 }
prep_minutes: 5
grade_bands: [6-8, 9-12]
materials:
  - "A printed Build-a-Brain board for each player"
  - "6 small coins per board, to be the messages between neurons"
  - "2 large coins, for the referee to toss"
printables:
  - title: "Build-a-Brain board and guide"
    file: printables/build-a-brain-coin-snap.pdf
    paper: a4
    color: color
    copies: "One board (page 1) per player. Page 2 is the guide."
    source: "https://cs4fndownloads.wordpress.com/build-a-brain-coin-snap/"
standards: ["MS-ALG-ML-06", "HS-SOC-HU-44"]
credits: "Created by Peter McOwan and Paul Curzon, Queen Mary University of London, for cs4fn and Teaching London Computing. Developed for the Royal Society Summer Science Exhibition 2016."
notice: "CS Offline is not affiliated with or endorsed by Queen Mary University of London, cs4fn, or Teaching London Computing."
license: "CC BY-NC-SA"
status: published
---

## What you'll do

Your brain is made of billions of nerve cells called neurons. Each one follows a simple rule about
when to fire, or send a message to the neurons it's connected to. In this activity you'll build a
tiny artificial brain, a neural network, out of a paper board and some coins. Then you'll use it to
play Coin Snap.

## The game

A referee tosses two coins. If they match, both heads or both tails, the first player to shout
"Snap!" gets a point. Shout "Snap!" when they don't match and you lose a point.

## How it works

1. **Load the messages.** Put a small coin on each red circle. These coins are the messages your
   neurons send.
2. **Toss.** The referee tosses two large coins and places them on the yellow circles.
3. **Fire the sensory neurons.** Each sensory neuron watches one coin and fires if it sees heads, or
   if it sees tails. When a neuron fires, slide its small coin along the line to the neuron it's
   connected to.
4. **Fire the relay neurons.** A relay neuron fires only when it has received two coins.
5. **Fire the motor neuron.** The motor neuron fires if it gets even one coin. When it fires, you
   are its mouth: shout "Snap!"
6. **Reset.** Move all the small coins back to the red circles and play again.

Play against a friend, each with your own board, and see whose brain is faster.

## Afterward

- Your brain shouted "Snap!" at the right times. Did it understand the game?
- What does each relay neuron detect? What does the motor neuron detect?
- How would you rewire the brain to shout "Snap!" only when the coins are different?
- This brain was wired by people. How could a brain learn the wiring on its own?

This activity is from [cs4fn](https://cs4fndownloads.wordpress.com/build-a-brain-coin-snap/) by
Peter McOwan and Paul Curzon.
