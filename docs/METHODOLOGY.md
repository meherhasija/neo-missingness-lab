# Research Methodology

## 1. Introduction

The project focuses on machine learning-based classification of Potentially Hazardous Asteroids (PHAs).

The main focus is to study how missing asteroid diameter measurements affect classification performance and to compare different techniques for handling missing values.

The research also examines whether diameter availability is related to absolute magnitude and discovery period.

## 2. Related Research

Previous studies have explored the use of machine learning techniques for classifying potentially hazardous asteroids.

- Nair and Babu (2025) used Random Forest techniques for Near-Earth Object hazard classification.
- Malakouti et al. (2023) compared different machine learning algorithms, including Extra Trees, Random Forest, LightGBM, Gradient Boosting and AdaBoost, for dangerous asteroid classification.

These studies provide background for applying machine learning to asteroid hazard classification. This project extends the investigation by focusing on missing diameter measurements and comparing different missing-data handling strategies.

## 3. Dataset Collection

The dataset is obtained from the NASA/JPL Small-Body Database.

File used: `data/neo_asteroid_dataset.csv`

The dataset contains 42,815 records and 21 columns.

Out of these records, 42,680 have valid PHA labels. The remaining 135 records with missing PHA labels are excluded from supervised classification.

The labelled dataset contains:

- 40,130 non-PHA records.
- 2,550 PHA records.

The positive class represents approximately 5.97% of the labelled dataset.

Diameter is missing in 41,569 records of the original dataset, which represents approximately 97.09%.

## 4. Data Preprocessing

The following preprocessing steps are performed:

1. The CSV dataset is loaded using Pandas.
2. The dataset is checked for missing values.
3. Records with missing PHA labels are excluded from supervised classification.
4. PHA values are converted into numerical labels, where N = 0 and Y = 1.
5. The required orbital and diameter features are selected.
6. Unnecessary identifiers and unsuitable columns are excluded.
7. The dataset is divided into training and testing sets.

The columns `H` and `moid` are not used as predictive features because they are directly related to PHA classification criteria.

They are retained for separate analysis and verification.

## 5. Feature Selection

The main experiments use the following six features:

| Feature | Description |
|---|---|
| a | Semi-major axis |
| e | Orbital eccentricity |
| i | Orbital inclination |
| om | Longitude of ascending node |
| w | Argument of perihelion |
| diameter | Asteroid diameter |

For the orbital-only experiment, diameter is removed and only the five orbital features are used.

## 6. Train-Test Split

The labelled dataset is divided using an 80:20 stratified split.

- Training records: 34,144
- Testing records: 8,536
- Random state: 42

Stratification is used to maintain the class distribution in both sets.

The preprocessing methods are fitted using training data to avoid using information from the test set during imputation.

## 7. Machine Learning Model

The main experiments use HistGradientBoostingClassifier.

The model parameters are:

- Maximum iterations: 100
- Learning rate: 0.1
- Class weight: Balanced
- Random state: 42
- Early stopping: Disabled

Balanced class weights are used because the dataset contains considerably fewer PHA records than non-PHA records.

## 8. Missing-Data Handling Techniques

Six different methods are compared.

### M1: Native Missing-Value Handling

The model's built-in missing-value handling is used without applying a separate imputation technique.

### M2: Median Imputation

Missing values are replaced with the median calculated from the training data.

### M3: Median Imputation with Missingness Indicator

Median imputation is combined with an additional binary column that indicates whether the original diameter value was missing.

### M4: KNN Imputation

The missing diameter values are estimated using the five nearest neighbours.

The orbital features are scaled before calculating distances. Training records with known diameter values are used as neighbours.

### M5: Iterative Imputation

Iterative imputation is performed using Bayesian Ridge regression.

The method estimates missing values by using relationships between the selected features.

### M6: Complete-Case Analysis

Only records with complete values for all six selected features are retained.

This method uses fewer records than the other methods.

## 9. Orbital-Only Experiment (M7)

An additional experiment is performed using only the five orbital features:

- a
- e
- i
- om
- w

Diameter is excluded completely.

The same HistGradientBoostingClassifier configuration is used.

This experiment helps compare classification performance with and without diameter information.

## 10. Random Forest Experiment

A separate Random Forest classifier is implemented using the same six selected features.

The model uses 300 trees, balanced class weights, and random state 42.

Median imputation with missingness indicators is used before classification.

Two classification thresholds are compared:

1. Default threshold of 0.50.
2. A threshold selected using five-fold stratified out-of-fold predictions on the training data.

The selected threshold is approximately 0.1233.

The threshold is selected to maximise recall while maintaining a minimum precision of 20% on the training out-of-fold predictions.

The final test set is not used for threshold selection.

## 11. Model Evaluation

The following evaluation metrics are used:

**Accuracy:** Measures the proportion of correct predictions.

**Precision:** Measures how many predicted PHA records are actually PHA records.

**Recall:** Measures how many actual PHA records are correctly identified.

**F1-score:** Combines precision and recall into a single measure.

**ROC-AUC:** Measures the ability of the model to distinguish between the two classes across different thresholds.

**Average Precision:** Summarises precision-recall performance and is useful for imbalanced datasets.

Confusion matrices are also used to examine true positives, true negatives, false positives, and false negatives.

## 12. Repeated Evaluation

The experiments are repeated using 10 stratified train-test splits.

The base random state is 42.

The mean and standard deviation of the evaluation metrics are calculated to study how model performance changes across different splits.

M6 is evaluated separately because it uses only complete records.

## 13. Bootstrap Analysis

Bootstrap analysis is used to examine uncertainty in model evaluation.

The notebook performs:

- 200 bootstrap iterations for metric confidence intervals within each split.
- 1,000 paired bootstrap iterations for comparisons between methods.

The results are used to examine the variability of performance metrics and differences between methods.

## 14. Missingness Pattern Analysis

Diameter availability is studied across different absolute magnitude groups.

The dataset is divided into four groups:

- H ≤ 18
- 18 < H ≤ 20
- 20 < H ≤ 22
- H > 22

For each group, the total number of records, available diameter values, and missing diameter values are calculated.

PHA rates are also compared between records with available and missing diameter.

This analysis helps identify whether diameter missingness is distributed equally across different asteroid groups.

## 15. Discovery Period Analysis

The `first_obs` column is used to group asteroids according to their discovery decade.

The number of records with available and missing diameter is calculated for each decade.

This helps examine changes in diameter availability across discovery periods.

The results are interpreted carefully because some decades have smaller sample sizes.

## 16. MOID Analysis

A simplified rule based on MOID ≤ 0.05 AU is evaluated against the existing PHA labels.

The rule is compared using accuracy, precision, recall, F1-score, and a confusion matrix.

The analysis produces 20,607 false positives and achieves 100% recall.

This demonstrates that MOID alone is not sufficient to reproduce the existing PHA classification.

The rule is used only for analysis and does not replace the original PHA labels.

## 17. NASA/JPL Record Verification

Two groups of records are selected for additional verification.

### Verification of 17 MOID Disagreements

Seventeen records with PHA = N, MOID ≤ 0.05 AU, and H ≤ 22 are checked using the NASA/JPL SBDB API.

All 17 records returned a current PHA flag of False.

### Verification of 33 Records with H > 22

Thirty-three records with PHA = Y and H > 22 are checked using the individual SBDB API and the SBDB Query API.

All 33 returned a current PHA flag of True.

H uncertainty information was available for eight records. All eight reported uncertainty intervals included H = 22.

These checks are used to examine selected records and retain the original PHA labels.

## 18. Implementation

The project is implemented using Python and Google Colab.

The main notebook is:

`notebooks/NEO_Complete.ipynb`

The separate Random Forest notebook is:

`notebooks/Random_Forest_PHA_Baseline.ipynb`

Both notebooks load the dataset directly from the GitHub raw CSV file.

The generated analysis files are saved in the Colab output directory and downloaded as ZIP files.

The output CSV files are uploaded to the GitHub results folders.

NASA/JPL API requests are used for selected verification analyses, so an internet connection is required.

## 19. Testing

The repository contains Python source files for loading CSV data and calculating missingness summaries.

The tests are located in:

`tests/test_diagnostics.py`

GitHub Actions is configured to run the tests whenever changes are pushed to the main branch or a pull request is created.

The workflow has completed successfully.

These tests check the diagnostics functionality. They do not execute the complete machine learning notebooks.

## 20. Limitations

1. A large proportion of diameter measurements are missing.
2. The PHA class is highly imbalanced.
3. Complete-case analysis uses fewer records.
4. Missingness patterns show associations but do not prove causation.
5. Model results depend on the dataset and experimental settings.
6. The models classify existing PHA labels and do not predict actual asteroid impacts.
7. NASA/JPL API responses may change over time.

## 21. Conclusion

The methodology compares different missing-data handling techniques and studies their effect on PHA classification.

The experiments also examine orbital-only classification, Random Forest threshold selection, repeated evaluation, bootstrap analysis, and missingness patterns across absolute magnitude groups and discovery periods.

The additional NASA/JPL verification analyses help examine selected records where simplified classification rules and existing PHA labels differ.

The overall methodology provides a comparison of missing-data strategies and highlights the importance of understanding missingness when applying machine learning to astronomical datasets.

## 22. References

1. NASA/JPL Small-Body Database (SBDB). https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html

2. NASA/JPL Small-Body Database Query API. https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html

3. NASA/JPL Small-Body Database API. https://ssd-api.jpl.nasa.gov/doc/sbdb.html

4. Nair, R. R., & Babu, T. (2025). *Effective Hazard Categorization of Near-Earth Objects with Random Forest Techniques.* Procedia Computer Science, 259, 1682–1692. https://doi.org/10.1016/j.procs.2025.04.123

5. Malakouti, S. M., Menhaj, M. B., & Suratgar, A. A. (2023). *Machine Learning Techniques for Classifying Dangerous Asteroids.* MethodsX, 11, 102337. https://doi.org/10.1016/j.mex.2023.102337
