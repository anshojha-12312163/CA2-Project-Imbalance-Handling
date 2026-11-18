# CA2 Project: Imbalance-Handling Strategies on Small, Imbalanced Medical Data

Dataset: Pima Indians Diabetes (768 rows, 8 features, 268 positive / 500 negative).
Source: UCI / National Institute of Diabetes and Digestive and Kidney Diseases.

## Folder layout
- data/pima_diabetes.csv   complete dataset (with header row added)
- code/run_experiments.py  complete, executable source code
- results/                 tables (CSV) and figures (PNG) produced by the code
- paper/                   put your own research paper here (PDF/DOCX)
- requirements.txt

## How to run
    pip install -r requirements.txt
    python code/run_experiments.py
Runtime is a few minutes on a normal laptop (no GPU needed).

## What the code does
1. Loads the data, treats impossible zeros (Glucose, BloodPressure, SkinThickness, Insulin, BMI) as missing, median-imputes, standardises.
2. Repeats 20 random stratified 70/30 splits.
3. Shrinks the training set to 60, 120, 250 and full (537) samples with only 25% minority class (artificially small and imbalanced).
4. Compares 6 strategies x 2 classifiers (Logistic Regression, Random Forest):
   Baseline, Class Weights, Random Oversampling, Random Undersampling, SMOTE, Borderline-SMOTE.
5. Reports Balanced Accuracy, Macro F1, G-mean and minority recall (mean and std over 20 runs), plus a paired Wilcoxon test against Baseline.
Resampling is done inside the pipeline, so it is applied to training data only (no leakage into the test set).
