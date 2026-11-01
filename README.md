# Machine Learning-Based Classification of Potentially Hazardous Near-Earth Objects

## About the Project

This project studies the classification of Potentially Hazardous Asteroids (PHAs) using machine learning. The main focus is on understanding how missing asteroid diameter measurements affect classification performance.

A large portion of the dataset does not contain diameter values. Instead of simply removing these records, this project compares different ways of handling missing data and examines how each approach affects the model's predictions.

The aim is to understand whether the choice of missing-data handling method changes the classification of potentially hazardous Near-Earth Objects (NEOs).

## Research Question

How does the missingness of asteroid diameter measurements affect machine learning-based PHA classification, and how do different missing-data handling strategies compare?

## Dataset

The dataset was obtained from the NASA/JPL Small-Body Database (SBDB).

- Total records: 42,815
- Records with available PHA labels: 42,680
- Non-PHA records: 40,130
- PHA records: 2,550
- Records with missing diameter: 41,569
- Percentage of missing diameter values: approximately 97.09%

All records in the dataset are Near-Earth Objects.

**Target variable:** `pha`

- `Y`: Potentially Hazardous Asteroid
- `N`: Not classified as a Potentially Hazardous Asteroid

The dataset is available in the `data` folder.

## Features Used

The following six features are used for classification:

| Feature | Description |
|---|---|
| a | Semi-major axis |
| e | Orbital eccentricity |
| i | Orbital inclination |
| om | Longitude of ascending node |
| w | Argument of perihelion |
| diameter | Asteroid diameter |

The columns `moid` and `H` were excluded because they are directly related to the criteria used to identify potentially hazardous asteroids. They could introduce target leakage into the model.

Identifiers and other unsuitable or highly incomplete columns were also excluded.

## Methodology

The dataset was cleaned by removing records with missing target labels. An 80:20 stratified train-test split was used with a random state of 42.

Six missing-data handling strategies were evaluated using the same HistGradientBoostingClassifier configuration.

### Experiments

| ID | Method | Description |
|---|---|---|
| M1 | Native Missing-Value Handling | Uses the model's built-in handling of missing values |
| M2 | Median Imputation | Replaces missing diameter values with the median |
| M3 | Median Imputation with Missingness Indicator | Adds an indicator to identify originally missing diameter values |
| M4 | KNN Imputation | Estimates missing values using the 5 nearest neighbours |
| M5 | Iterative Imputation | Uses Bayesian Ridge regression to estimate missing values iteratively |
| M6 | Complete-Case Analysis | Uses only records with complete feature values |

A Random Forest model was also implemented as an additional algorithmic baseline. Threshold tuning was explored to examine the effect of class imbalance on hazardous asteroid detection.

## Experimental Setup

The following settings were used for the six main experiments:

- Algorithm: HistGradientBoostingClassifier
- Maximum iterations: 100
- Learning rate: 0.1
- Random state: 42
- Class weighting: Balanced
- Train-test split: 80:20
- Stratification: Enabled

For a fair comparison, the six methods were also evaluated on a common test subset containing 247 complete-feature records. This allowed their predictions to be compared on the same test observations.

## Results

### Comparison on the Common Test Subset

The following results are based on the same 247 test records for all six methods.

| Method | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| M1 Native | 55.06% | 39.55% | 94.59% | 0.5578 | 0.7643 |
| M2 Median | 53.04% | 38.71% | 97.30% | 0.5538 | 0.7454 |
| M3 Median + Indicator | 51.01% | 37.95% | 100.00% | 0.5502 | 0.7764 |
| M4 KNN | 58.70% | 39.39% | 70.27% | 0.5049 | 0.6982 |
| M5 Iterative | 55.87% | 38.85% | 82.43% | 0.5281 | 0.6822 |
| M6 Complete-Case | 76.11% | 62.71% | 50.00% | 0.5564 | 0.7763 |

M1 achieved the highest F1-score among the six methods on the common test subset. M3 achieved the highest ROC-AUC and recall.

Complete-case analysis achieved higher accuracy and precision, but its recall was lower. These results show why accuracy alone is not sufficient when evaluating an imbalanced classification problem.

The complete-case model was trained using fewer training records than the other methods, so its results should be interpreted with this difference in mind.

## Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Average Precision

Recall is particularly important in this study because missing a potentially hazardous asteroid may be more concerning than incorrectly flagging a non-PHA object.

## Repository Structure

The project files are organised into the following folders:
- data/: Contains the NASA asteroid dataset.
- notebooks/: Contains the seven Jupyter notebooks used for the experiments.
- results/metrics/: Contains evaluation metrics for each experiment.
- results/predictions/: Contains the model predictions.
- results/: Contains the combined comparison of all six missing-data methods.
- src/: Source code for the project.
- tests/: Test files.
- docs/: Project documentation.

## How to Run the Project

Clone the repository from GitHub.
Open the project folder in VS Code or Jupyter Notebook.
Install the required Python libraries using requirements.txt.
Open the required experiment notebook from the notebooks/ folder.
Make sure the dataset is available in the data/ folder.

Run the notebook cells in order.
Make sure the dataset is available in the `data` folder when running the notebooks locally. If using Google Colab, upload the dataset or update the dataset path accordingly.

## Limitations

- Diameter measurements are missing for approximately 97.09% of the dataset.
- The availability of diameter measurements is associated with differences in the observed PHA distribution. This may reflect selection effects in the available observations.
- The dataset contains an imbalanced target variable, with considerably fewer PHA records.
- The complete-case experiment uses a much smaller subset of the available data.
- The results depend on the dataset snapshot, selected features, model configuration and train-test split.

## Conclusion

This project compares six approaches to handling missing asteroid diameter measurements in PHA classification.

The experiments show that different missing-data strategies produce different classification results. Native missing-value handling and median imputation with a missingness indicator provide useful alternatives, while complete-case analysis illustrates the limitations of discarding records with missing values.

The study highlights the importance of examining missing-data patterns and using multiple evaluation metrics when building classification models for imbalanced datasets.

## References

1. NASA/JPL Small-Body Database Query API: https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html
2. NASA/JPL Small-Body Database API: https://ssd-api.jpl.nasa.gov/doc/sbdb.html
3. Malakouti et al. (2023). *Machine learning techniques for classifying dangerous asteroids*. MethodsX, 11, 102337.
4. Nair and Babu (2025). *Effective Hazard Categorization of Near-Earth Objects with Random Forest Techniques*. Procedia Computer Science, 259, 1682-1692.

---

**Project Repository:** https://github.com/meherhasija/neo-missingness-lab
