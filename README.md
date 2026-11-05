# Machine Learning-Based Classification of Potentially Hazardous Near-Earth Objects

## Introduction

This project focuses on classifying Potentially Hazardous Asteroids (PHAs) using machine learning techniques. The main objective is to study how missing asteroid diameter measurements affect classification performance.

The dataset contains a large number of missing diameter values. Different missing-data handling techniques are applied and compared to understand how they influence model performance.

The project also examines the relationship between diameter availability, absolute magnitude, and discovery period.

**Research Question:**

How does selection bias associated with missing asteroid diameter measurements affect machine learning classification of potentially hazardous Near-Earth Asteroids, and how do different missing-data strategies compare?

## Related Research

Two research papers were referred to while developing this project:

1. *Effective Hazard Categorization of Near-Earth Objects with Random Forest Techniques* (Nair and Babu, 2025) uses Random Forest for classifying hazardous and non-hazardous Near-Earth Objects.
2. *Machine Learning Techniques for Classifying Dangerous Asteroids* (Malakouti et al., 2023) compares different machine learning classifiers, including Random Forest, Extra Trees, LightGBM, Gradient Boosting, and AdaBoost.

These papers provide background on applying machine learning to asteroid hazard classification. Our project focuses further on the effect of missing diameter measurements and compares different strategies for handling missing data.

## Objectives

1. To study the missing values present in the asteroid dataset.
2. To apply different techniques for handling missing diameter values.
3. To compare machine learning models using different evaluation metrics.
4. To study the effect of missing diameter measurements on classification performance.
5. To compare diameter-based classification with an orbital-only model.
6. To analyse diameter availability across different absolute magnitude groups and discovery periods.
7. To verify selected asteroid records using NASA/JPL data.
8. To evaluate the consistency of model performance using repeated evaluation and bootstrap analysis.

## Dataset

The dataset is obtained from the NASA/JPL Small-Body Database.

Dataset file: `data/neo_asteroid_dataset.csv`

The dataset contains 42,815 records and 21 columns.

| Description | Count |
|---|---:|
| Total records | 42,815 |
| Total columns | 21 |
| Records with PHA label | 42,680 |
| PHA records (Y) | 2,550 |
| Non-PHA records (N) | 40,130 |
| Records with missing PHA label | 135 |
| Records with missing diameter | 41,569 |

Approximately 97.09% of the original dataset has missing diameter values.

All records belong to the Near-Earth Object category (`neo = Y`).

The target variable is `pha`, which indicates whether an asteroid is classified as potentially hazardous.

- Y: Potentially Hazardous Asteroid
- N: Not classified as a Potentially Hazardous Asteroid

Records with missing PHA labels are excluded from supervised classification.

## Features Used

The following six features are used in the main experiments:

| Feature | Description |
|---|---|
| a | Semi-major axis |
| e | Orbital eccentricity |
| i | Orbital inclination |
| om | Longitude of ascending node |
| w | Argument of perihelion |
| diameter | Asteroid diameter |

The columns `H` and `moid` are excluded from the predictive models because they are directly related to PHA classification criteria and could introduce target leakage.

They are used separately for analysing missingness patterns and verifying selected records.

## Methodology

The labelled dataset is divided into training and testing sets using an 80:20 stratified split with random state 42.

The main experiments use the HistGradientBoostingClassifier with 100 iterations, a learning rate of 0.1, balanced class weights, and early stopping disabled.

Different methods are used to handle missing diameter values.

| Method | Description |
|---|---|
| M1 - Native Handling | Uses the model's built-in handling of missing values. |
| M2 - Median Imputation | Replaces missing values with the median calculated from the training data. |
| M3 - Median + Indicator | Uses median imputation and an additional column to indicate missing diameter values. |
| M4 - KNN Imputation | Estimates missing diameter values using the five nearest neighbours. |
| M5 - Iterative Imputation | Uses Bayesian Ridge regression to estimate missing values iteratively. |
| M6 - Complete-Case Analysis | Uses only records with complete values for all selected features. |
| M7 - Orbital-Only | Uses five orbital features without diameter. |

A separate Random Forest experiment is also performed. It compares the default classification threshold of 0.50 with a threshold selected using five-fold out-of-fold predictions on the training data.

## Evaluation Metrics

The models are evaluated using the following metrics:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Average Precision

Since the dataset is imbalanced, precision and recall are also considered instead of relying only on accuracy.

## Results and Analysis

### Main Model Results

The following results are obtained on the fixed test set containing 8,536 records.

| Method | Accuracy | Precision | Recall | F1-score | ROC-AUC | Average Precision |
|---|---:|---:|---:|---:|---:|---:|
| M1 Native | 77.33% | 16.31% | 67.65% | 0.2629 | 0.8135 | 0.2653 |
| M2 Median | 76.91% | 16.04% | 67.65% | 0.2593 | 0.8155 | 0.2628 |
| M3 Median + Indicator | 77.00% | 15.84% | 66.08% | 0.2556 | 0.8129 | 0.2781 |
| M4 KNN | 76.23% | 15.11% | 64.51% | 0.2449 | 0.7937 | 0.2028 |
| M5 Iterative | 76.49% | 15.55% | 66.27% | 0.2520 | 0.8030 | 0.2068 |
| M7 Orbital-Only | 75.28% | 15.16% | 68.24% | 0.2480 | 0.7970 | 0.1939 |

M1 achieves the highest F1-score among M1-M5. M3 gives the highest Average Precision, while M2 gives the highest ROC-AUC among these methods.

M7 achieves the highest recall in this comparison, showing that orbital features can identify a considerable proportion of PHA records even without diameter.

M6 is evaluated separately because it uses only complete records. Its test set contains 247 records, so its results are not directly comparable with the full test set.

### Repeated Evaluation

The experiments are also repeated using 10 stratified train-test splits.

The mean F1-score, ROC-AUC, and Average Precision are calculated to examine the consistency of the results.

M1 achieves the highest mean F1-score and ROC-AUC among the full-test-set methods in the repeated evaluation.

### Missingness Analysis

Diameter availability is compared across absolute magnitude groups.

| H Group | Total Records | Diameter Available | Diameter Missing | Availability |
|---|---:|---:|---:|---:|
| H ≤ 18 | 1,092 | 392 | 700 | 35.90% |
| 18 < H ≤ 20 | 3,765 | 435 | 3,330 | 11.55% |
| 20 < H ≤ 22 | 6,889 | 274 | 6,615 | 3.98% |
| H > 22 | 30,932 | 143 | 30,789 | 0.46% |

The results show that diameter availability decreases considerably across higher absolute magnitude groups.

The PHA rates of records with available and missing diameter are also compared within each group.

The analysis suggests that diameter missingness is associated with other asteroid characteristics and should not automatically be treated as random.

### Discovery Period Analysis

The dataset is also grouped by discovery decade to compare diameter availability over different periods.

The results show differences in diameter availability across discovery periods. Some decades contain fewer observations, so their percentages should be interpreted carefully.

### MOID Analysis and Verification

A simplified rule using MOID ≤ 0.05 AU is compared with the existing PHA labels.

The rule achieves 100% recall but has only 11.01% precision because it produces 20,607 false positives.

This shows that MOID alone is not sufficient to reproduce the existing PHA classification.

Selected records are also checked using NASA/JPL SBDB APIs:

- 17 records with MOID ≤ 0.05 AU, H ≤ 22, and PHA = N were verified. All 17 returned a current PHA flag of False.
- 33 records with PHA = Y and H > 22 were verified. All 33 returned a current PHA flag of True.

The original PHA labels are retained.

### Random Forest Results

The Random Forest experiment compares the default threshold with a threshold selected using training out-of-fold predictions.

The selected threshold is approximately 0.1233.

| Metric | Default Threshold | Tuned Threshold |
|---|---:|---:|
| Accuracy | 94.20% | 86.53% |
| Precision | 85.71% | 21.78% |
| Recall | 3.53% | 48.43% |
| F1-score | 0.0678 | 0.3005 |
| ROC-AUC | 0.7983 | 0.7983 |
| Average Precision | 0.2658 | 0.2658 |

The tuned threshold improves recall considerably, although precision and accuracy decrease.

## Conclusion

The project shows that different missing-data handling techniques produce different classification results.

Native missing-value handling and median-based approaches provide competitive performance in the main experiments. The analysis also shows that diameter availability varies across absolute magnitude groups and discovery periods.

The orbital-only experiment demonstrates that orbital features provide useful information even when diameter is unavailable.

Overall, the study highlights the importance of understanding missing-data patterns before applying machine learning techniques to astronomical datasets.

## Limitations

1. Approximately 97.09% of the original dataset has missing diameter values.
2. The PHA class represents only about 5.97% of the labelled records.
3. Complete-case analysis uses a much smaller dataset.
4. The observed missingness patterns do not establish causation.
5. The models classify existing PHA labels and do not predict actual asteroid impacts.
6. NASA/JPL API information may change over time.

## Technologies Used

- Python
- Google Colab
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- NASA/JPL Small-Body Database API
- GitHub

## Repository

https://github.com/meherhasija/neo-missingness-lab

## References

1. NASA/JPL Small-Body Database: https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html
2. NASA/JPL SBDB Query API: https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html
3. NASA/JPL SBDB API: https://ssd-api.jpl.nasa.gov/doc/sbdb.html
4. Nair, R. R., & Babu, T. (2025). *Effective Hazard Categorization of Near-Earth Objects with Random Forest Techniques.* Procedia Computer Science, 259, 1682–1692. https://doi.org/10.1016/j.procs.2025.04.123
5. Malakouti, S. M., Menhaj, M. B., & Suratgar, A. A. (2023). *Machine Learning Techniques for Classifying Dangerous Asteroids.* MethodsX, 11, 102337. https://doi.org/10.1016/j.mex.2023.102337
