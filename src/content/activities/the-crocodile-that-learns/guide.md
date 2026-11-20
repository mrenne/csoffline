---
---

## Overview

Students play Hexapawn, a three-by-three game of pawns, against a "paper computer". The computer
chooses each move by drawing a token at random from a card that shows the current board. After each
game it is rewarded or punished: a losing move loses a token, and a winning move gains one. Over
10 to 20 games the losing moves disappear and the computer becomes very hard to beat. This is
reinforcement learning, the same idea behind AI systems that learned to play Go and video games.

## Preparing

- Print pages 1–6 for each pair. Pages 3–5 are the move cards and don't need cutting out: lay the
  sheets flat in front of the crocodile player.
- Cut out the six pieces on page 2 and the paper tokens on page 6. Pairs need 19 blue, 17 orange,
  8 green and 3 purple tokens to start, plus spares. Tokens are a colour and a shape, so the PDF
  works printed in black and white.
- Counters or beads work too. If you use sweets, as the original activity suggests, check your
  school's food and allergy rules first.
- Keep page 7, the answer key, for yourself.

## The move cards

There are 19 cards, one for every board the crocodiles can face: 2 for their first move, 10 for
their second and 7 for their third. Each card shows the board after the monkeys have moved, with
the crocodiles at the top. Boards that are mirror images of each other share one card, so students
sometimes need to flip a card in their heads. Show them the mirror rule on page 1 before they play.

The crocodiles never need a fourth move: every game is over by then.

## Running the activity

1. Teach the movement rules with one practice game where both players choose their own moves.
2. Have pairs set up the cards and tokens, then play at least 10 games, filling in the learning log.
3. Remind the monkey players to play to win every time. A crocodile that only ever plays a weak
   opponent learns less.
4. To start simpler, skip the reward rule and only take tokens away when the crocodiles lose. This
   still works, just a little more slowly.
5. If time allows, have pairs swap roles and start a fresh crocodile.

## What the trained crocodile looks like

Hexapawn is a win for the second player: if the crocodiles play perfectly, the monkeys can never
win. The answer key on page 7 greys out the moves that a perfect monkey player can always beat.
Some things to know:

- **Card 6 can run out of tokens.** Both of its moves lose. When the crocodiles reach it with an
  empty card, they give up, and the token from their previous move is taken away instead. This is
  how the crocodile learns to avoid card 6 altogether.
- **Card 17 has only one move, and it loses.** The crocodile learns to avoid this board too.
- On card 1, only the capture (green) is safe. A trained crocodile always takes it.

The original activity says a card can never run out of tokens. It can, so this version adds the
"give up" rule, which is also how Martin Gardner's original Hexapawn learning machine worked.

## Debrief

- **Plot the learning.** Have pairs share their learning logs and compare when the crocodiles
  started winning. Each crocodile learned at a different speed, because the draws were random and
  each monkey player played differently.
- **Reward and punishment.** The computer never knew why a move was good. It only learned that some
  moves were followed by wins and others by losses. This is called a **reward signal**.
- **The blame problem.** Only the crocodiles' last move was punished, even when an earlier move was
  the real mistake. Working out which earlier moves deserve credit or blame is a hard problem in
  reinforcement learning, called **credit assignment**. Card 6 shows it in action: the computer
  eventually blames the move that led there.
- **Limits.** The computer learned to beat one opponent in one tiny game. What would change in a
  game like chess, which has far too many boards to fit on cards?
- **Real systems.** Programs like AlphaGo learned partly by playing millions of games against
  themselves, using neural networks instead of cards to estimate which moves are good.

## History

The game is Hexapawn, invented by Martin Gardner in 1962 to show how a machine made of matchboxes
and beads could learn. Gardner based it on Donald Michie's MENACE, a matchbox computer that learned
noughts and crosses (tic-tac-toe) in 1961. cs4fn turned the idea into the Sweet Learning Computer,
and Annabel Lindner and Stefan Seegerer adapted that for AI Unplugged as Beat the Crocodile.

## Going further

- [AI Unplugged](https://www.aiunplugged.org/) by Annabel Lindner and Stefan Seegerer has the
  original activity and others. Its rule-based crocodile chess activity pairs well with this one, to
  compare a computer that follows rules people wrote with one that learns.
- cs4fn's [Sweet Learning Computer](http://www.cs4fn.org/machinelearning/sweetlearningcomputer.php)
  is a version of the same game.
