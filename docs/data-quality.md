# Notes on document data and evaluation

My current document-understanding work has made dataset quality a practical
engineering concern. These notes describe the checks I want a document dataset to
support; they do not report a deployed classifier's accuracy.

## Separate the stages

```text
Original file -> extraction or OCR -> text -> classification -> organization
```

A readable PDF, an accurate transcription, and a correct category are separate
questions. Summarization would be another component. A classification label alone
does not establish the factual contents of a document.

## Give labels clear boundaries

An invoice requests payment; a receipt records a payment. A marksheet describes
assessed results; a completion certificate can have a different purpose. Mixed
documents and unfamiliar types need an explicit review path.

## Keep related examples together

A digital document, its scan, and an edited copy are related observations. Assign
them a common group before splitting data. Generated examples that share a
template also need grouping. A split seed cannot fix duplicate leakage.

## Use generated data for the right questions

Synthetic examples help exercise schemas, parsers, labeling rules, and training
code. Held-out templates still share a generator. Real-world performance needs a
separate, permitted, representative evaluation set rather than a claim based only
on generated examples.

## Make the next run explainable

Track source permissions, extraction method/version, hashes, label provenance,
and split assignments. Fit learned preprocessing on training examples only.
Report category-level errors and inspect examples where the model is uncertain.

Related work: [Filewise extraction](projects/filewise.md),
[ML fundamentals](projects/ml-fundamentals.md), and the
[project roadmap](https://github.com/SiddharthaGanguli/multimodal-smart-file-organizer/blob/main/TODO.md).

[Back to profile](../README.md)
