# ECG application foundation

[Repository](https://github.com/jeet-biswas/ECG_analysis) |
[Reviewed source snapshot](https://github.com/jeet-biswas/ECG_analysis/tree/f525abae28dfbae0f215717e4d6c87dbed123483)

This project establishes application structure around an intended ECG-analysis
workflow. Its implemented work is currently the web and authentication foundation.

## Implemented layers

| Layer | Present in the source |
|---|---|
| Frontend | React and Vite application structure |
| Authentication UI | Firebase signup, login, password reset, and Google login |
| Backend | FastAPI application with SQLAlchemy user endpoints |
| ML workspace | Directories and placeholder files reserved for later work |

Keeping these layers distinct makes it easier to understand which part of an
application is ready and which part still needs implementation and validation.

## Boundary of this portfolio entry

The reviewed ECG ingestion, validation, training, model configuration, DVC, and
test files are placeholders. This entry therefore makes no claim about an ECG
classifier, diagnostic performance, clinical validation, or a working medical
decision system.

## Development priorities

A useful next milestone would define permitted sample signals, a reproducible
input format, and signal-validation tests before adding a model. Model evaluation
would then need independent data and an explicit intended use. Application
authentication and model quality should be tested as separate concerns.

[Back to profile](../../README.md)
