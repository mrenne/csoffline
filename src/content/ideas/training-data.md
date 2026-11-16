---
name: Training data
domains: [ai-literacy, data-science]
student_summary: AI systems learn from examples. The examples they get shape what they can do.
related: [classification, bias]
---

## What's really going on

Many AI systems aren't programmed with rules. Instead they learn patterns from huge sets of examples called training data. A system that learns to recognize cats studies thousands of labeled cat photos. Whatever is in those examples, good or bad, shapes what the AI can do. If something is missing from the training data, the AI will struggle with it.

## Background

In machine learning, a model learns its behavior from training data rather than from hand-written rules. The data's size, quality, labeling, and coverage determine what the model can do; gaps lead to errors on underrepresented cases, and patterns in the data, including unfair ones, get learned along with everything else. Good practice keeps separate test data to check performance on examples the model hasn't seen. Unplugged sorting and labeling activities help students see that people decide what goes into the data and how it's labeled.

## Misconceptions

- AI learns like a person and understands its examples. Models detect statistical patterns; they don't understand meaning.
- Once trained, an AI is objective. A model reflects the choices, gaps, and biases in its training data.
- Testing on the training examples shows how good the model is. A model can memorize its training data and still fail on new examples.
