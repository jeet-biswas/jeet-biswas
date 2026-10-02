# How I approach an engineering task

I use the following questions to move from a prototype toward something another
person can inspect, run, and improve. They are a working approach, not a claim
that every earlier notebook already meets every step.

## Define the observable behavior

Start with an input, an expected output, and the conditions under which the
operation should fail. For document extraction, a saved file and successfully
extracted text are two different outcomes. For binary search, an insertion point
and an exact match are two different contracts.

## Keep a small boundary between parts

Separate parsing from storage and UI state. A parser should expose text and a
status that can be tested without signing into a browser. An algorithm function
should expose its result without requiring a notebook's previous cells.

## Check assumptions before adding complexity

Use simple examples and known expected results first. Then test empty input,
corrupt input, duplicates, interruptions, or revoked access as appropriate to the
component. Compare an optimized algorithm with a simple reference on small cases.

## Preserve provenance

Record where data came from, which transformation produced it, and what version
was tested. Separate generated data from real observations. A reproducible run
should make it possible to explain a change without guessing what changed locally.

## Review the user-facing result

Clear retries and honest status labels matter alongside the successful path.
Look at the actual preview, output, or interaction and document the limitations
that affect how it should be used.

Examples: [Filewise](projects/filewise.md), [DSA](projects/dsa.md), and
[the difference between displayed history and model context](projects/chatbot.md).

[Back to profile](../README.md)
