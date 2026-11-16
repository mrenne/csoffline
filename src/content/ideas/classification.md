---
name: Classification
domains: [ai-literacy]
student_summary: Sorting things into groups by their features, the way many AI systems make decisions.
related: [training-data]
---

## What's really going on

Classification means sorting things into groups based on their features. A spam filter sorts email into spam and not spam, and a photo app sorts pictures by the faces in them. Many AI systems learn to classify by studying lots of labeled examples and finding the features that separate one group from another. When the examples or the features are poor, the system makes mistakes, sometimes with confidence.

## Background

Classification is a type of supervised machine learning: a model learns from labeled examples to assign new items to categories. Common uses include spam filtering, medical image screening, and content moderation. Unplugged, students can build a decision tree or a set of sorting rules from example cards, then test it on new cards to see where it fails. That surfaces the key ideas of features, training versus testing, and accuracy.

## Misconceptions

- The AI understands what it's classifying. A classifier finds statistical patterns in features; it has no idea what a cat or a spam email is.
- A high accuracy score means the classifier is good for everyone. Overall accuracy can hide much worse performance for some groups or rare cases.
- Categories are natural and obvious. People choose the categories and the labels, and those choices shape what the system can do.
