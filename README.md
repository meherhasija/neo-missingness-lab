# Machine Learning-Based Classification of Potentially Hazardous Near-Earth Objects

## 1. About the Project

This project investigates how missing asteroid diameter measurements affect Machine Learning-based classification of Potentially Hazardous Asteroids (PHAs).

The dataset contains a large number of missing diameter values. Instead of removing all incomplete records, this study compares different missing-data handling strategies and examines their effect on classification performance.

The project also investigates whether diameter availability is associated with differences in the observed PHA distribution and whether these patterns vary across asteroid discovery periods.

## 2. Research Question

How does selection bias associated with missing asteroid diameter measurements affect Machine Learning-based classification of potentially hazardous near-Earth asteroids, and how do different missing-data handling strategies compare?

## 3. Dataset

The dataset was obtained from the NASA/JPL Small-Body Database (SBDB).

| Dataset property | Value |
|---|---:|
| Total records | 42,815 |
| Records with PHA labels | 42,680 |
| Non-PHA records | 40,130 |
| PHA records | 2,550 |
| Missing diameter values | 41,569 |
| Missing diameter percentage | 97.09% |

All records in the dataset are Near-Earth Objects.

**Target variable:** `pha`

- `Y`: Classified as a Potentially Hazardous Asteroid.
- `N`: Not classified as a Potentially Hazardous Asteroid.

The dataset is stored in the `data/` directory.

## 4. Features Used

The six main features used in the experiments are:

| Feature | Description |
|---|---|
| a | Semi-major axis |
| e | Orbital eccentricity |
| i | Orbital inclination |
| om | Longitude of ascending node |
| w | Argument of perihelion |
| diameter | Asteroid diameter |

The columns `moid` and `H` were excluded because they are directly related to the official PHA classification criteria and could introduce target leakage.

Identifiers and unsuitable or highly incomplete columns were also excluded.

An additional orbital-only experiment used five orbital features: `a`, `e`, `i`, `om`, and `w`, without diameter.

## 5. Methodology

Records without PHA target labels were excluded from supervised model training.

The dataset was divided using an 80:20 stratified train-test split with `random_state=42`.

The six main missing-data strategies were evaluated using `HistGradientBoostingClassifier`.

### Main experiments

| ID | Method | Description |
|---|---|---|
| M1 | Native Missing-Value Handling | Uses the model's built-in missing-value handling |
| M2 | Median Imputation | Replaces missing diameter values with the median |
| M3 | Median + Missingness Indicator | Adds an indicator for originally missing diameter values |
| M4 | KNN Imputation | Estimates missing values using the 5 nearest neighbours |
| M5 | Iterative Imputation | Uses Bayesian Ridge regression for iterative estimation |
| M6 | Complete-Case Analysis | Uses only records with complete feature values |

### Additional experiment

**M7: Orbital-Only Baseline**

This experiment uses only the five orbital features and excludes diameter. It helps examine how classification performance changes when diameter is not used as a predictor.

### Model configuration

- Algorithm: HistGradientBoostingClassifier
- Maximum iterations: 100
- Learning rate: 0.1
- Random state: 42
- Class weighting: Balanced
- Early stopping: Disabled
- Train-test split: 80:20
- Stratification: Enabled

## 6. Experimental Results

### 6.1 Full Test Set Comparison

M1–M5 were evaluated on the full test set of 8,536 records. M6 uses only complete cases and therefore cannot be directly compared on this full test set.

| Method | Accuracy | Precision | Recall | F1-score | ROC-AUC | AP |
|---|---:|---:|---:|---:|---:|---:|
| M1 Native | 77.33% | 16.31% | 67.65% | 0.2629 | 0.8135 | 0.2653 |
| M2 Median | 76.91% | 16.04% | 67.65% | 0.2593 | 0.8155 | 0.2628 |
| M3 Median + Indicator | 77.00% | 15.84% | 66.08% | 0.2556 | 0.8129 | 0.2781 |
| M4 KNN | 76.23% | 15.11% | 64.51% | 0.2449 | 0.7937 | 0.2028 |
| M5 Iterative | 76.49% | 15.55% | 66.27% | 0.2520 | 0.8030 | 0.2068 |

M1 achieved the highest F1-score among these five methods. M2 achieved the highest ROC-AUC, while M3 achieved the highest Average Precision.

### 6.2 Measured-Diameter Test Subset

This comparison uses the same 247 test records with available diameter measurements.

| Method | Accuracy | Precision | Recall | F1-score | ROC-AUC | AP |
|---|---:|---:|---:|---:|---:|---:|
| M1 Native | 61.13% | 42.95% | 90.54% | 0.5826 | 0.8002 | 0.6487 |
| M2 Median | 58.70% | 41.25% | 89.19% | 0.5641 | 0.7820 | 0.6086 |
| M3 Median + Indicator | 60.73% | 42.86% | 93.24% | 0.5872 | 0.8103 | 0.6695 |
| M4 KNN | 62.35% | 41.28% | 60.81% | 0.4918 | 0.7081 | 0.4540 |
| M5 Iterative | 63.16% | 43.41% | 75.68% | 0.5517 | 0.7264 | 0.4685 |
| M6 Complete-Case | 76.11% | 62.71% | 50.00% | 0.5564 | 0.7763 | 0.6329 |

M3 achieved the highest F1-score, recall, ROC-AUC and Average Precision among the six methods on this subset. M6 achieved the highest accuracy and precision but had lower recall.

### 6.3 Missing-Diameter Test Subset

This comparison uses 8,289 test records without diameter measurements.

| Method | Accuracy | Precision | Recall | F1-score | ROC-AUC | AP |
|---|---:|---:|---:|---:|---:|---:|
| M1 Native | 77.81% | 14.19% | 63.76% | 0.2322 | 0.7992 | 0.1825 |
| M2 Median | 77.45% | 14.01% | 63.99% | 0.2299 | 0.7995 | 0.1921 |
| M3 Median + Indicator | 77.49% | 13.63% | 61.47% | 0.2231 | 0.7961 | 0.1936 |
| M4 KNN | 76.64% | 13.73% | 65.14% | 0.2268 | 0.7951 | 0.1838 |
| M5 Iterative | 76.89% | 13.80% | 64.68% | 0.2274 | 0.7980 | 0.1793 |
| M7 Orbital-Only | 75.61% | 13.69% | 68.58% | 0.2282 | 0.7997 | 0.1769 |

M3 achieved the highest Average Precision among the missing-data methods. M7 achieved slightly higher ROC-AUC and recall, showing that orbital-only features can provide useful classification information even when diameter is unavailable.

### 6.4 Repeated Evaluation

The experiments were also evaluated across 10 stratified splits.

For M1 on the full test set, the repeated evaluation produced:

- Mean F1-score: 0.2642 ± 0.0090
- Mean ROC-AUC: 0.8199 ± 0.0088
- Mean Average Precision: 0.2667 ± 0.0139

M1 achieved the highest mean among the three reported metrics in the repeated full-test comparison. These results provide additional evidence about variation across splits, but do not establish a universal best method.

## 7. Missingness Analysis

Diameter values are missing for approximately 97.09% of the dataset.

The relationship between diameter availability and PHA labels was investigated.

| Diameter status | Non-PHA | PHA | PHA rate |
|---|---:|---:|---:|
| Missing | 39,224 | 2,210 | 5.33% |
| Available | 906 | 340 | 27.29% |

The observed PHA rate is considerably higher among records with measured diameters.

This indicates that diameter availability is associated with differences in the observed dataset. It may reflect selection effects, but the analysis does not establish a causal relationship.

### 7.1 Analysis by Absolute Magnitude (H)

Diameter availability was also examined across H categories.

| H category | Total records | Diameter available | Availability |
|---|---:|---:|---:|
| H ≤ 18 | 1,092 | 392 | 35.90% |
| 18 < H ≤ 20 | 3,765 | 435 | 11.55% |
| 20 < H ≤ 22 | 6,889 | 274 | 3.98% |
| H > 22 | 30,932 | 143 | 0.46% |

The results show a strong decline in diameter availability as H increases.

### 7.2 Discovery-Era Analysis

Diameter availability was examined according to the decade of first observation.

The analysis showed a substantial decline in measured-diameter availability across discovery periods:

- 1990s: 18.02%
- 2000s: 6.32%
- 2010s: 3.12%
- 2020s: approximately 0.01%

The 2020s measured group contains only one record, so it should not be treated as a reliable estimate. Earlier decades also contain relatively small numbers of records.

These patterns suggest that diameter availability is associated with discovery era and observation history. They do not establish causation.

## 8. Investigation of 33 PHA Records with H > 22

The dataset contained 33 records labelled `PHA = Y` despite having H values above 22.

These records were investigated using the NASA/JPL SBDB APIs.

The checks found:

- All 33 records returned `PHA = True` through the individual Object API.
- All 33 appeared in the current PHA group returned by the Query API.
- All 33 were also identified as NEOs.
- Original and JPL H values matched.
- Original and JPL MOID values were nearly identical.
- Eight records had reported H uncertainty values.
- All eight reported uncertainty intervals included H = 22.
- The other 25 records did not have reported H uncertainty values.

The official CNEOS PHA definition specifies both MOID ≤ 0.05 AU and H ≤ 22. The current SBDB API results therefore present an apparent consistency issue that remains unresolved in this study.

The records were not automatically relabelled or removed.

The investigation files are stored in `results/analysis/`.

## 9. Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Average Precision

Average Precision and hazardous-class recall are particularly important because the dataset is imbalanced and missing a potentially hazardous asteroid may be more concerning than incorrectly flagging a non-PHA object.

The PHA label represents an existing classification, not the probability that an asteroid will impact Earth.

## 10. Repository Structure

- `data/`: Dataset used in the experiments.
- `notebooks/`: Jupyter notebooks for the experiments and evaluation.
- `results/metrics/`: Model evaluation metrics.
- `results/predictions/`: Model predictions.
- `results/analysis/`: Missingness analysis, discovery-era analysis and JPL verification results.
- `src/`: Project source code.
- `tests/`: Test files.
- `docs/`: Project documentation.

## 11. Limitations

- Approximately 97.09% of diameter values are missing.
- Diameter availability is associated with differences in the observed PHA distribution.
- The target variable is imbalanced.
- Complete-case analysis uses a much smaller subset.
- The experiments depend on the dataset snapshot, selected features, model configuration and data split.
- The repeated evaluation uses a finite number of splits.
- The original dataset retrieval date and exact original API query provenance have not been fully established.
- The apparent discrepancy involving 33 PHA-labelled records with H > 22 remains unresolved.
- The study identifies associations and does not establish causal relationships.

## 12. Conclusion

This project investigates how missing asteroid diameter measurements affect PHA classification using multiple missing-data handling strategies.

The results show that different strategies produce different classification outcomes. Native missing-value handling and median imputation with missingness indicators provide useful approaches, while complete-case analysis demonstrates the limitations of discarding records with missing values.

The missingness analysis also shows that diameter availability is associated with H categories, discovery periods and differences in observed PHA rates.

The investigation of 33 records with H > 22 provides an additional data-validation finding that requires further clarification.

Overall, the study highlights the importance of understanding missing-data patterns, preventing target leakage and using multiple evaluation metrics when developing classification models for imbalanced astronomical datasets.

## 13. References

1. NASA/JPL Small-Body Database Query API: https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html
2. NASA/JPL Small-Body Database API: https://ssd-api.jpl.nasa.gov/doc/sbdb.html
3. NASA CNEOS, Near-Earth Object Groups: https://cneos.jpl.nasa.gov/about/neo_groups.html
4. Malakouti et al. (2023). *Machine learning techniques for classifying dangerous asteroids*. MethodsX, 11, 102337.
5. Nair and Babu (2025). *Effective Hazard Categorization of Near-Earth Objects with Random Forest Techniques*. Procedia Computer Science, 259, 1682–1692.

**Project Repository:** https://github.com/meherhasija/neo-missingness-lab
