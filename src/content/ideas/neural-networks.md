---
name: Neural Networks
domains: [ai-literacy]
student_summary: Lots of simple connected parts that pass signals to each other, loosely inspired by the brain.
related: [classification, training-data]
---

## What's really going on

A neural network is made of many simple parts, called neurons, connected together. Each neuron
follows one simple rule: if it gets enough signal from the neurons feeding into it, it fires and
passes a signal on. No single neuron is smart, but a big network of them can recognize faces,
understand speech, or play games. Modern AI systems like chatbots and image generators are built
from huge neural networks with billions of connections.

## Background

Artificial neural networks are loosely modeled on biological neurons. Each artificial neuron adds up
its weighted inputs and fires (or produces a stronger output) when the total passes a threshold. The
networks are arranged in layers: input, hidden, and output. Instead of being wired by hand, most
networks learn by adjusting their connection weights to reduce errors on training data. Unplugged
networks with fixed rules, where students pass tokens between neurons, make the layers and
thresholds visible before students meet the idea of learning.

## Misconceptions

- A neural network is a digital brain that thinks like a person. It is loosely inspired by the brain
  but works very differently, and it has no understanding of what it's doing.
- Someone programs the rules for each neuron. In most real networks, people design the structure and
  the network learns its weights from data.
- If you look inside a neural network you can see why it made a decision. Large networks are hard to
  interpret, and explaining their decisions is an active research area.
