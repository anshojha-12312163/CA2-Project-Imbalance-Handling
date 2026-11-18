# Paper outline (follow Dr. Sabha's format). WRITE THE TEXT YOURSELF.

The text must be your own words (AI content under 10%). This file only tells you what each section needs.

Title: choose one that names the problem, the data and the comparison.
Abstract (150-200 words): problem, data, methods compared, key numbers from results/, one-line conclusion.
Keywords: 4-5 (small data, imbalanced data, SMOTE, diabetes prediction ...).

1. Introduction
   - Why imbalanced + small medical data is hard (missing minority cases is costly).
   - Gap: which strategy works best when data gets smaller?
   - Key contributions (3-4 bullets) and Paper structure paragraph (as in the reference paper).
2. Background / Related Work
   2.1 Class imbalance: data-level, algorithm-level, hybrid (read the reference paper's Sect. 2 and cite the SAME kinds of sources; find 8-12 papers yourself).
   2.2 Small data and overfitting.
3. Data and Methods
   3.1 Dataset (table: rows, features, class counts; use results/fig_class_distribution.png)
   3.2 Preprocessing (zeros as missing, median imputation, scaling)
   3.3 Introducing small + imbalanced training sets (sizes 60/120/250/537, 25% minority)
   3.4 Methods compared (explain each of the 6 strategies and 2 classifiers)
   3.5 Testing procedure (20 stratified 70/30 splits, resampling inside training only)
4. Performance Metrics: Balanced Accuracy, Macro F1, G-mean, minority recall (give formulas).
5. Experimentation and Results
   - Implementation details (library versions, hyperparameters from the code)
   - Tables from results/summary_mean.csv; figures fig_metrics_vs_size_*.png and fig_minority_recall_smallest.png
   - Wilcoxon results (wilcoxon_vs_baseline_BA.csv); note splits overlap, so treat p-values as indicative.
   - Discuss: what changes as size shrinks, accuracy vs minority-recall trade-off, why Random Forest and Logistic Regression behave differently.
6. Conclusion: findings, limitations (one dataset, small test sets, no hyperparameter tuning), future work.
References: only papers you actually read (include SMOTE, Borderline-SMOTE, the dataset source, imbalanced-learn, scikit-learn).

Before submitting: check every number in your paper against results/, and run your own similarity/AI check.
