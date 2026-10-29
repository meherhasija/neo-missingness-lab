# NEO Missingness Lab

An open-source research toolkit for studying how missing asteroid measurements affect machine-learning evaluation for Near-Earth Object (NEO) classification.

**Status:** Initial project scaffold. Research experiments and scientific conclusions are not yet validated.

## Goals
- Retrieve and snapshot data from the NASA/JPL Small-Body Database API.
- Audit missingness and compare measured vs. unmeasured asteroid records.
- Compare missing-data strategies using leakage-safe evaluation.
- Report precision-recall metrics and uncertainty, not accuracy alone.

## Current scope
This repository is being developed around the research question:

> How does selection bias caused by missing asteroid diameter measurements affect machine-learning classification of potentially hazardous near-Earth asteroids?

The repository does **not** predict asteroid impacts and is not an operational hazard-warning system.

## Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Project layout

```text
neo-missingness-lab/
├── data/                  # Local datasets; not committed
├── docs/                  # Research notes and methodology
├── notebooks/             # Exploratory notebooks
├── src/neo_missingness/   # Reusable project code
├── tests/                 # Automated tests
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Data and reproducibility

Do not commit large raw datasets or private credentials. Store the dataset snapshot locally and record:
- source URL and API parameters
- retrieval timestamp
- record count and field list
- checksum/hash
- validation results

Use the official JPL API documentation to verify supported parameters before running a download.

## Scientific safeguards
- Never impute the target label.
- Fit imputers and preprocessing on training folds only.
- Keep the final test set out of model selection.
- Compare methods on clearly defined, comparable evaluation sets.
- Report precision, recall, F1, average precision / PR-AUC, ROC-AUC, and confusion matrices.
- Treat missingness as potentially systematic, not automatically random.
- Do not claim a research gap is novel until relevant literature and existing repositories have been checked.

## Development

Run tests:

```bash
pytest
```

## Open-source contribution plan
1. Publish the repository with this scaffold.
2. Add the validated data snapshot workflow.
3. Implement missingness diagnostics and evaluation methods.
4. Add controlled experiments and tests.
5. Document verified results and limitations.

## License
Released under the MIT License. See `LICENSE`.
