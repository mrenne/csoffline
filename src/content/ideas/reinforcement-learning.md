---
name: Reinforcement Learning
domains: [ai-literacy]
student_summary: Learning by trial and error, getting rewarded for good results and punished for bad ones.
related: [training-data, neural-networks]
---

## What's really going on

Reinforcement learning is how a computer can learn to do something without anyone showing it how.
It tries actions, sometimes at random, and gets a reward when things go well and a penalty when they
go badly. Over many tries, it makes the actions that led to rewards more likely and the ones that
led to penalties less likely. This is how AI systems have learned to play board games like Go and
chess, play video games, and control robots, often by practicing millions of times.

## Background

In reinforcement learning, an **agent** takes **actions** in an **environment** and receives a
**reward** signal. Its goal is to choose actions that earn the most reward over time. The agent
keeps a **policy**, a way of choosing an action in each situation, and updates it from experience.
Unlike learning from labeled examples, nobody tells the agent the right answer: it only finds out
how things turned out, often much later. Deciding which earlier actions deserve credit or blame for
a result is called the **credit assignment problem**. Agents also have to balance **exploration**
(trying new actions to learn more) with **exploitation** (using what already works). Unplugged
versions, where tokens stand for how likely each move is, date back to Donald Michie's MENACE, a
matchbox computer that learned noughts and crosses in 1961.

## Misconceptions

- The computer understands the game or works out a strategy. It only changes how likely each action
  is, based on rewards. It has no idea why a move is good.
- A bad move is deleted after one failure. In most real systems, an action that leads to a penalty
  just becomes less likely, because it might still be good in other situations.
- The reward goes to the action that caused it. The agent often can't tell which of its many
  earlier actions mattered, so rewards are shared out over the actions that came before.
- Reinforcement learning works quickly. Real systems usually need huge amounts of practice, which
  is why many are trained in simulations or by playing against themselves.
