---
---

## Overview

Students act out a small neural network on a paper board, using coins as the messages between
neurons, and use it to play Coin Snap. The board shows that a network of very simple units, each
following one rule, can produce behavior that looks smart. The activity is a two-page PDF from cs4fn
with the board and a short guide.

## How the network works

The board has seven neurons in three layers:

| Neurons | Count | Rule |
| --- | --- | --- |
| Sensory | 4 | Each watches one coin and fires on heads or on tails (Coin 1 heads, Coin 1 tails, Coin 2 heads, Coin 2 tails). |
| Relay | 2 | Each fires when it gets 2 messages: one combines the two "heads" neurons, the other the two "tails" neurons. |
| Motor | 1 | Fires on 1 message, which means shouting "Snap!" |

The relay neurons work like AND (both heads, or both tails), and the motor neuron works like OR
(either relay fired). Together the network fires only when the coins match.

| Coin 1 | Coin 2 | Heads relay | Tails relay | Snap? |
| --- | --- | --- | --- | --- |
| Heads | Heads | Fires | — | Yes |
| Tails | Tails | — | Fires | Yes |
| Heads | Tails | — | — | No |
| Tails | Heads | — | — | No |

## Running the activity

- Print page 1 (the board) for each player. The PDF is A4, so print it with "Fit to page" on Letter
  paper. Each player needs 6 small coins, and the referee needs 2 large ones.
- Have students first play a round of Coin Snap with their own brains, then play it with the board.
- In groups of three, two players race each other's boards while the third is the referee.

## Debrief

- The network plays perfectly, but nothing in it understands the game. Where does the "smartness"
  come from?
- The **threshold** is the number of messages a neuron needs before it fires. What happens to the
  network's behavior if a relay neuron's threshold drops to 1?
- This network was designed by people. Real neural networks learn their own connection strengths,
  called weights, from training data. How might this one learn?

## Notes on the PDF

- The guide says "neutron" once where it means "neuron."
- It says the yellow circles are the positions the "motor neurons" focus on. It means the sensory
  neurons.

## Going further

- The [Brain-in-a-bag activity](https://teachinglondoncomputing.org/resources/inspiring-unplugged-classroom-activities/the-brain-in-a-bag-activity/)
  from Teaching London Computing has students act as the neurons themselves to play Red-black Snap.
- cs4fn's [Build a brain to play snap](https://www.cs4fn.org/ai/snap/) page has more on the idea.
- [Learning about Machine Learning](https://teachinglondoncomputing.org/machine-learning/) from
  Teaching London Computing collects related activities.
