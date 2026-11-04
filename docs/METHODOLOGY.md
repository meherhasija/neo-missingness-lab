# Research Methodology

## 1. Research Question

How does selection bias associated with missing asteroid diameter measurements affect Machine Learning-based classification of potentially hazardous near-Earth asteroids, and how do different missing-data handling strategies compare?

## 2. Dataset Description

The dataset was obtained from the NASA/JPL Small-Body Database (SBDB).

- Total records: 42,815
- Records with valid PHA labels: 42,680
- Non-PHA records: 40,130
- PHA records: 2,550
- Records with missing diameter: 41,569
- Diameter missingness: 97.09%

Records with missing target labels were excluded from supervised model evaluation.

The target variable is `pha`, where Y represents a PHA classification and N represents a non-PHA classification.

All records in the dataset are Near-Earth Objects.

## 3. Feature Selection

### 3.1 Main Features

The main experiments used:

1. `a` – Semi-major axis
2. `e` – Orbital eccentricity
3. `i` – Orbital inclination
4. `om` – Longitude of ascending node
5. `w` – Argument of perihelion
6. `diameter` – Asteroid diameter

### 3.2 Excluded Features

- `pha`: Used as the target variable, not as a predictor.
- `moid`: Excluded because it is directly involved in the official PHA definition.
- `H`: Excluded because it is directly involved in the official PHA definition.
- Identifiers: Excluded because they identify objects rather than provide suitable predictive measurements.
- `q`: Excluded because it is redundant with other orbital parameters.
- `albedo`: Excluded because approximately 97% of its values are missing.

Diameter was retained because missing diameter measurements are the central subject of the research.

## 4. Data Preprocessing

1. Records without PHA target labels were removed.
2. The remaining labelled records were used for supervised learning.
3. A stratified 80:20 train-test split was created.
4. The split used `random_state=42`.
5. The test set contained 8,536 records, including 510 PHA records.
6. Preprocessing and imputation were performed according to the requirements of each experimental method.

The target variable was not imputed.

## 5. Main Experimental Methods

Six missing-data strategies were evaluated.

### M1: Native Missing-Value Handling

The HistGradientBoostingClassifier was used with its native missing-value handling capability.

### M2: Median Imputation

Missing diameter values were replaced with the median diameter calculated from the training data.

### M3: Median Imputation with Missingness Indicator

Median imputation was combined with an additional indicator feature that records whether the original diameter value was missing.

### M4: KNN Imputation

KNN imputation was performed using five nearest neighbours. Orbital features were scaled using training data, and only training records with known diameter values were used as donors.

### M5: Iterative Imputation

Iterative imputation was performed using Bayesian Ridge regression within a StandardScaler pipeline.

### M6: Complete-Case Analysis

Records containing missing values in the selected features were removed.

The complete-case model was evaluated on 247 test records. Its results are therefore not directly comparable with methods evaluated on the full test set.

## 6. Model Configuration

The six main experiments used the following configuration:

- Model: HistGradientBoostingClassifier
- Maximum iterations: 100
- Learning rate: 0.1
- Random state: 42
- Class weighting: Balanced
- Early stopping: False

The same main classifier configuration was used to compare the different missing-data strategies.

## 7. Evaluation Procedure

The main train-test evaluation used a stratified 80:20 split.

M1–M5 were evaluated on the full test set of 8,536 records.

The methods were additionally evaluated on:
- The measured-diameter subset: 247 records.
- The missing-diameter subset: 8,289 records.

M6 was evaluated only on the complete-case test subset of 247 records.

The following metrics were calculated:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Average Precision

Average Precision and recall were given particular attention because the PHA class represents approximately 5.98% of the labelled dataset.

## 8. Orbital-Only Baseline (M7)

An additional experiment was performed without using asteroid diameter.

The predictors were:

- `a`
- `e`
- `i`
- `om`
- `w`

The same HistGradientBoostingClassifier configuration was used.

This experiment provides a comparison for understanding the contribution of diameter-related information and the performance of orbital features when diameter is unavailable.

## 9. Repeated Evaluation and Bootstrap Analysis

The evaluation was extended using 10 stratified splits.

Performance metrics were collected across the repeated experiments to examine variation between splits.

Bootstrap analyses were also performed to examine uncertainty in model comparisons and paired differences.

The bootstrap summaries are descriptive and should not be interpreted as formal independent-sample significance tests.

## 10. Missingness Analysis

The availability of diameter measurements was investigated against the existing PHA labels.

### 10.1 Diameter Availability and PHA Distribution

- Missing diameter group: 39,224 non-PHA and 2,210 PHA records.
- Available diameter group: 906 non-PHA and 340 PHA records.
- PHA rate among records with missing diameter: 5.33%.
- PHA rate among records with available diameter: 27.29%.

These differences indicate an association between diameter availability and the observed PHA distribution.

### 10.2 Analysis by H Categories

Diameter availability and PHA rates were compared across four H categories:

1. H ≤ 18
2. 18 < H ≤ 20
3. 20 < H ≤ 22
4. H > 22

Diameter availability declined substantially as H increased.

The analysis was used to investigate whether missingness patterns differ across absolute-magnitude categories.

### 10.3 Discovery-Era Analysis

The `first_obs` field was used to group records by discovery decade.

Diameter availability and PHA rates were compared between measured and unmeasured groups across decades.

The analysis showed a decline in diameter availability in more recent discovery periods.

Some decades contain small sample sizes, and the 2020s measured group contains only one record. These small groups should not be used to make strong statistical conclusions.

The analysis identifies associations and does not establish that discovery era causes diameter missingness.

## 11. Investigation of 33 PHA Records with H > 22

The dataset contained 33 records with `pha = Y` and H values above 22.

These records were investigated using two NASA/JPL SBDB API methods.

### 11.1 Individual Object API Verification

Each of the 33 objects was queried individually.

The verification checked:

- Object name
- NEO classification
- PHA classification
- Absolute magnitude H
- MOID
- Orbital solution information
- Available physical-parameter uncertainty information

All 33 records returned `PHA = True` and `NEO = True`.

### 11.2 Query API Cross-Check

The SBDB Query API was queried using the current PHA group filter.

The query returned 2,550 asteroid records.

All 33 investigated objects were found in the current query results, and all had `pha = Y`.

### 11.3 H Uncertainty Analysis

Of the 33 records:

- Eight had reported H uncertainty values.
- Twenty-five did not have reported H uncertainty values.
- All eight reported uncertainty intervals included H = 22.

The missing uncertainty values for the remaining records were treated as unavailable information, not as zero uncertainty.

### 11.4 Interpretation

The official CNEOS PHA definition specifies both MOID ≤ 0.05 AU and H ≤ 22.

However, both current SBDB API checks returned PHA classifications for all 33 records despite their H values being above 22.

The reason for this apparent discrepancy has not been established.

The records were retained without automatically changing their labels. The discrepancy is documented as a data-validation finding requiring further clarification.

## 12. Random Forest Baseline

A Random Forest baseline was also implemented separately.

Threshold tuning was explored to examine the effect of class imbalance on hazardous-class detection.

The threshold-tuned and default Random Forest results should not be treated as a strictly controlled threshold-only comparison because their training procedures differed.

The Random Forest results are therefore treated as an additional exploratory baseline rather than a direct replacement for the six main experiments.

## 13. Research Safeguards and Limitations

The following considerations apply to the study:

- The target variable was not imputed.
- `moid` and `H` were excluded from the main predictor set to avoid direct target leakage.
- Imputation methods used training data for estimating missing values.
- Complete-case results were interpreted separately because of their smaller evaluation sample.
- Results were examined using multiple performance metrics rather than accuracy alone.
- Associations between missingness, H categories, discovery periods and PHA labels were not interpreted as causal evidence.
- The original dataset retrieval date and exact original API query provenance have not been fully established.
- The 33-record PHA/H discrepancy remains unresolved.
- Results depend on the dataset snapshot, features, model configuration and evaluation split.

## 14. Conclusion

The methodology compares six missing-data handling strategies and an additional orbital-only baseline for PHA classification.

It also investigates diameter availability across PHA groups, H categories and discovery decades.

The additional JPL API investigation provides a validation check for 33 records with H values above 22 that are nevertheless classified as PHA by the current API responses.

Together, these experiments examine the effect of missing measurements on classification performance and highlight the importance of data validation, leakage prevention and careful interpretation of imbalanced classification results.
