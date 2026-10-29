# Research methodology (draft)

## Primary question
How does selection bias caused by missing asteroid diameter measurements affect ML classification of potentially hazardous near-Earth asteroids?

## Planned comparisons
1. Native missing-value handling.
2. Median imputation.
3. Median imputation plus missingness indicators.
4. KNN imputation.
5. Iterative imputation.
6. Complete-case analysis.

These are planned experimental conditions, not completed findings. The implementation must ensure comparable evaluation sets and leakage-safe preprocessing.

## Required safeguards
- Keep unlabelled targets out of supervised training; never impute the target.
- Fit imputation and scaling inside each training fold.
- Keep a final holdout set out of model selection.
- Report class distribution and majority-class baseline.
- Prioritize average precision / PR-AUC and hazardous-class recall alongside precision, F1, ROC-AUC, and confusion matrix.
- Investigate whether measured and unmeasured groups differ systematically.
- Control training-set size when attributing differences to selection bias.
- Do not interpret associations as causal evidence.
- Treat the PHA flag as an existing classification label, not impact probability.

## Status
The methods and research question are provisional until the literature review, data validation, and experiments are complete.
