# Filewise: document extraction in a Drive library

Filewise is a collaborative file-organizing project. My merged contribution connects
document extraction to its Chrome extension so a saved document can also expose its
text. [Merged contribution: PR #20](https://github.com/SiddharthaGanguli/multimodal-smart-file-organizer/pull/20).

## The problem

Saving a PDF to Drive preserves the original, but does not by itself provide text
for previews, categorization, or future search. Extraction also needs a separate
failure state: a parser failure should not make a successful upload appear lost.

## The implementation

```text
Authorized Drive document
  -> Chrome extension
  -> local FastAPI companion
  -> TXT / DOCX / PDF extractor
  -> text, status, page references, and extraction provenance
  -> account-scoped preview in the extension
```

The same extractors support a standalone command-line JSON workflow. The extension
adds automatic extraction, retry, and text preview. It ties results to the connected
account and document version, invalidates stale text, and rechecks access before
showing a preview. The companion removes temporary copies after parsing.

## What to inspect

- [Extraction modules](https://github.com/SiddharthaGanguli/multimodal-smart-file-organizer/tree/main/app/extractors)
- [Architecture documentation](https://github.com/SiddharthaGanguli/multimodal-smart-file-organizer/blob/main/docs/architecture.md)
- [PR discussion and recorded validation](https://github.com/SiddharthaGanguli/multimodal-smart-file-organizer/pull/20)

The PR records parser, API, extension, and browser checks. Those are software
checks, not classification-accuracy measurements.

## Scope

This contribution extracts digital text and identifies pages that need OCR.
Actual OCR, document classification, and semantic search are later stages. PDF
reading order and tables remain limitations of plain-text extraction.

[Back to profile](../../README.md)
