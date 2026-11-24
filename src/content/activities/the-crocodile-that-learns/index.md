---
name: The Crocodile That Learns
domain: ai-literacy
summary: "Play a tiny chess game against a paper computer that picks its moves at random, then watch it learn from every win and loss until it can't be beaten."
ideas: [reinforcement-learning, training-data]
activity_type: board-game
audience: both
author:
  name: Annabel Lindner and Stefan Seegerer
  role: authors
  bio: "Annabel Lindner and Stefan Seegerer created AI Unplugged, a free collection of unplugged activities that explain how artificial intelligence works."
  link: { label: "Visit AI Unplugged", url: "https://www.aiunplugged.org/" }
group_size: { min: 2, max: 2 }
grouping: [pairs]
minutes: { min: 30, max: 45 }
prep_minutes: 15
grade_bands: [6-8, 9-12]
materials:
  - "Scissors, for cutting out the pieces and paper tokens"
  - "Optional: coloured counters, beads or wrapped sweets instead of paper tokens"
printables:
  - title: "Rules, board, move cards, tokens and answer key"
    file: printables/the-crocodile-that-learns.pdf
    paper: letter
    color: both
    copies: "Pages 1–6 for each pair: rules, board and pieces, three pages of move cards with the learning log, and tokens. Page 7 is the answer key."
standards: ["MS-ALG-ML-06", "HS-ALG-PS-04"]
credits: "Adapted by Mike Renne for CS Offline from Beat the Crocodile by Annabel Lindner and Stefan Seegerer (AI Unplugged), used under CC BY-NC 3.0. Their activity builds on cs4fn's Sweet Learning Computer, Martin Gardner's Hexapawn and Donald Michie's MENACE. Changes: a new title, new board, pieces, move cards and paper tokens, colour-and-shape tokens that work in black and white, a rule for when a card runs out of tokens, a learning log and an answer key."
notice: "Based on Beat the Crocodile by Annabel Lindner and Stefan Seegerer. CS Offline is not affiliated with or endorsed by AI Unplugged."
license: "CC BY-NC 3.0"
license_url: "https://creativecommons.org/licenses/by-nc/3.0/deed.en"
status: published
---

## What you'll do

Computers can learn to play games they've never been taught a strategy for. In this game, one of
you plays the monkeys and the other is a computer made of paper that plays the crocodiles. At
first the computer picks its moves completely at random. After every game it changes a few tokens,
and slowly it learns which moves win and which ones lose.

## The game

The board is three squares by three. Each side has three pieces, and every piece moves like a pawn
in chess:

- It moves one square straight forward into an empty square.
- It captures one square diagonally forward. It can't capture straight ahead.

You win if one of your pieces reaches the far row, if you capture every enemy piece, or if it's
the other side's turn and they can't move.

## How it works

1. **Set up.** The crocodile player lays out the move cards. Each card shows a board and every move
   the crocodiles could make, as coloured arrows. Put one matching token on each card for each arrow.
2. **Monkeys move.** The monkeys always go first and can make any legal move.
3. **Crocodiles move.** Find the card that matches the board. Close your eyes, pick a token from it,
   and make the move with the arrow of the same colour. Leave the token on the card's board picture.
4. **Learn.** When the game ends, the computer changes its tokens:
   - If the crocodiles lost, take away the token from their last move.
   - If the crocodiles won, add an extra token of that colour to their last move.
   - If a card has no tokens left, the crocodiles give up. Take away the token from the move before.
5. **Play again.** Put the tokens back on their cards and play another game. Keep a learning log of
   who wins.

Monkeys: try to win every game. The better you play, the faster the crocodile learns.

## Afterward

- Look at your learning log. When did the crocodiles start winning?
- Nobody told the computer a strategy. How did it get better?
- Some cards ended up with only one or two tokens. What do those tokens say about the moves?
- The computer only changed its last move after each game. Was that move always the one to blame?
- What would happen if the computer played a new monkey player who uses different moves?

This activity is adapted from Beat the Crocodile by Annabel Lindner and Stefan Seegerer, part of
[AI Unplugged](https://www.aiunplugged.org/).
