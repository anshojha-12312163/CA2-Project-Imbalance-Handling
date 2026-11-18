# Experimental Results & Performance Tables

This document contains evaluation tables generated from `results/all_runs.csv` over 20 repeated Monte Carlo stratified 70/30 splits.
Values are displayed as **Mean ± Standard Deviation**. The best performing mean in each column is highlighted in **bold**.

## Model: Logistic Regression (LogReg)

### Table: LogReg - Training Size: N = 60

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.684 ± 0.026 | 0.676 ± 0.024 | 0.633 ± 0.040 | 0.448 ± 0.070 |
| ClassWeight | **0.708 ± 0.035** | **0.713 ± 0.035** | **0.707 ± 0.040** | 0.649 ± 0.083 |
| RandomOver | 0.706 ± 0.033 | 0.710 ± 0.034 | 0.704 ± 0.036 | 0.644 ± 0.084 |
| RandomUnder | 0.677 ± 0.042 | 0.692 ± 0.040 | 0.688 ± 0.041 | **0.690 ± 0.092** |
| SMOTE | 0.704 ± 0.038 | 0.707 ± 0.037 | 0.701 ± 0.041 | 0.636 ± 0.083 |
| BorderlineSMOTE | 0.703 ± 0.036 | 0.708 ± 0.036 | 0.703 ± 0.040 | 0.648 ± 0.083 |

### Table: LogReg - Training Size: N = 120

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.675 ± 0.036 | 0.667 ± 0.031 | 0.615 ± 0.048 | 0.415 ± 0.069 |
| ClassWeight | **0.713 ± 0.035** | **0.718 ± 0.032** | **0.715 ± 0.032** | 0.667 ± 0.052 |
| RandomOver | 0.712 ± 0.037 | 0.716 ± 0.034 | 0.712 ± 0.035 | 0.660 ± 0.060 |
| RandomUnder | 0.708 ± 0.032 | 0.715 ± 0.029 | 0.713 ± 0.029 | **0.680 ± 0.050** |
| SMOTE | 0.709 ± 0.035 | 0.715 ± 0.031 | 0.711 ± 0.031 | 0.666 ± 0.059 |
| BorderlineSMOTE | 0.708 ± 0.034 | 0.714 ± 0.031 | 0.711 ± 0.030 | 0.664 ± 0.052 |

### Table: LogReg - Training Size: N = 250

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.694 ± 0.033 | 0.684 ± 0.029 | 0.638 ± 0.041 | 0.443 ± 0.058 |
| ClassWeight | **0.717 ± 0.023** | 0.724 ± 0.024 | 0.722 ± 0.025 | 0.684 ± 0.049 |
| RandomOver | 0.717 ± 0.025 | **0.724 ± 0.026** | **0.722 ± 0.027** | 0.685 ± 0.052 |
| RandomUnder | 0.714 ± 0.028 | 0.724 ± 0.029 | 0.721 ± 0.030 | 0.696 ± 0.062 |
| SMOTE | 0.714 ± 0.024 | 0.720 ± 0.024 | 0.718 ± 0.025 | 0.678 ± 0.056 |
| BorderlineSMOTE | 0.711 ± 0.025 | 0.721 ± 0.026 | 0.719 ± 0.026 | **0.696 ± 0.056** |

### Table: LogReg - Training Size: N = 537 (Full Training Set)

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.726 ± 0.031 | 0.716 ± 0.030 | 0.693 ± 0.037 | 0.543 ± 0.056 |
| ClassWeight | 0.727 ± 0.024 | 0.734 ± 0.026 | 0.732 ± 0.027 | 0.692 ± 0.055 |
| RandomOver | **0.728 ± 0.028** | **0.735 ± 0.030** | **0.733 ± 0.031** | 0.696 ± 0.057 |
| RandomUnder | 0.725 ± 0.026 | 0.733 ± 0.026 | 0.731 ± 0.027 | 0.698 ± 0.049 |
| SMOTE | 0.725 ± 0.027 | 0.731 ± 0.029 | 0.729 ± 0.030 | 0.689 ± 0.054 |
| BorderlineSMOTE | 0.716 ± 0.024 | 0.730 ± 0.026 | 0.729 ± 0.026 | **0.729 ± 0.052** |

### Balanced Accuracy Gain over Baseline (percentage points) - LogReg

| Method | N = 60 (pp) | N = 120 (pp) | N = 250 (pp) | Full (N = 537) (pp) |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.00 | 0.00 | 0.00 | 0.00 |
| ClassWeight | **+3.68** | **+5.06** | +4.03 | +1.80 |
| RandomOver | +3.43 | +4.87 | **+4.05** | **+1.95** |
| RandomUnder | +1.62 | +4.81 | +3.99 | +1.70 |
| SMOTE | +3.15 | +4.75 | +3.68 | +1.56 |
| BorderlineSMOTE | +3.23 | +4.62 | +3.72 | +1.37 |

---

## Model: Random Forest (RandomForest)

### Table: RandomForest - Training Size: N = 60

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.644 ± 0.037 | 0.641 ± 0.030 | 0.574 ± 0.052 | 0.363 ± 0.069 |
| ClassWeight | **0.701 ± 0.034** | 0.697 ± 0.034 | 0.682 ± 0.040 | 0.565 ± 0.073 |
| RandomOver | 0.672 ± 0.044 | 0.666 ± 0.041 | 0.632 ± 0.055 | 0.466 ± 0.084 |
| RandomUnder | 0.688 ± 0.037 | **0.706 ± 0.033** | **0.702 ± 0.034** | **0.720 ± 0.077** |
| SMOTE | 0.679 ± 0.043 | 0.674 ± 0.041 | 0.649 ± 0.053 | 0.507 ± 0.090 |
| BorderlineSMOTE | 0.675 ± 0.044 | 0.670 ± 0.042 | 0.645 ± 0.054 | 0.500 ± 0.089 |

### Table: RandomForest - Training Size: N = 120

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.650 ± 0.042 | 0.647 ± 0.035 | 0.580 ± 0.060 | 0.370 ± 0.082 |
| ClassWeight | **0.699 ± 0.033** | 0.693 ± 0.032 | 0.676 ± 0.039 | 0.548 ± 0.067 |
| RandomOver | 0.678 ± 0.039 | 0.671 ± 0.036 | 0.638 ± 0.048 | 0.470 ± 0.072 |
| RandomUnder | 0.696 ± 0.036 | **0.711 ± 0.033** | **0.709 ± 0.034** | **0.717 ± 0.066** |
| SMOTE | 0.685 ± 0.037 | 0.679 ± 0.035 | 0.657 ± 0.042 | 0.516 ± 0.072 |
| BorderlineSMOTE | 0.690 ± 0.036 | 0.684 ± 0.035 | 0.661 ± 0.042 | 0.517 ± 0.070 |

### Table: RandomForest - Training Size: N = 250

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.669 ± 0.031 | 0.661 ± 0.027 | 0.603 ± 0.041 | 0.394 ± 0.054 |
| ClassWeight | **0.715 ± 0.024** | 0.710 ± 0.025 | 0.697 ± 0.031 | 0.579 ± 0.057 |
| RandomOver | 0.691 ± 0.034 | 0.683 ± 0.032 | 0.654 ± 0.044 | 0.492 ± 0.067 |
| RandomUnder | 0.710 ± 0.024 | **0.726 ± 0.022** | **0.725 ± 0.022** | **0.736 ± 0.039** |
| SMOTE | 0.712 ± 0.027 | 0.706 ± 0.028 | 0.691 ± 0.035 | 0.564 ± 0.060 |
| BorderlineSMOTE | 0.702 ± 0.035 | 0.697 ± 0.034 | 0.681 ± 0.043 | 0.555 ± 0.070 |

### Table: RandomForest - Training Size: N = 537 (Full Training Set)

| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.722 ± 0.021 | 0.714 ± 0.020 | 0.699 ± 0.024 | 0.571 ± 0.039 |
| ClassWeight | 0.735 ± 0.022 | 0.740 ± 0.023 | 0.737 ± 0.025 | 0.688 ± 0.048 |
| RandomOver | 0.729 ± 0.025 | 0.728 ± 0.025 | 0.723 ± 0.026 | 0.642 ± 0.040 |
| RandomUnder | 0.733 ± 0.017 | **0.747 ± 0.017** | **0.747 ± 0.017** | **0.753 ± 0.036** |
| SMOTE | **0.741 ± 0.025** | 0.743 ± 0.024 | 0.740 ± 0.025 | 0.681 ± 0.037 |
| BorderlineSMOTE | 0.734 ± 0.019 | 0.738 ± 0.019 | 0.736 ± 0.020 | 0.690 ± 0.040 |

### Balanced Accuracy Gain over Baseline (percentage points) - RandomForest

| Method | N = 60 (pp) | N = 120 (pp) | N = 250 (pp) | Full (N = 537) (pp) |
| :--- | :---: | :---: | :---: | :---: |
| Baseline | 0.00 | 0.00 | 0.00 | 0.00 |
| ClassWeight | +5.59 | +4.66 | +4.91 | +2.55 |
| RandomOver | +2.52 | +2.41 | +2.21 | +1.40 |
| RandomUnder | **+6.49** | **+6.43** | **+6.50** | **+3.30** |
| SMOTE | +3.37 | +3.23 | +4.55 | +2.87 |
| BorderlineSMOTE | +2.97 | +3.69 | +3.64 | +2.41 |

---

## Overall Summary: Gain in Balanced Accuracy over Baseline

| Model | Training Size | Method | Baseline Mean BA | Method Mean BA | Gain (pp) |
| :--- | :---: | :--- | :---: | :---: | :---: |
| LogReg | 60 | Baseline | 0.676 | 0.676 | 0.00 |
| LogReg | 60 | ClassWeight | 0.676 | 0.713 | +3.68 |
| LogReg | 60 | RandomOver | 0.676 | 0.710 | +3.43 |
| LogReg | 60 | RandomUnder | 0.676 | 0.692 | +1.62 |
| LogReg | 60 | SMOTE | 0.676 | 0.707 | +3.15 |
| LogReg | 60 | BorderlineSMOTE | 0.676 | 0.708 | +3.23 |
| LogReg | 120 | Baseline | 0.667 | 0.667 | 0.00 |
| LogReg | 120 | ClassWeight | 0.667 | 0.718 | +5.06 |
| LogReg | 120 | RandomOver | 0.667 | 0.716 | +4.87 |
| LogReg | 120 | RandomUnder | 0.667 | 0.715 | +4.81 |
| LogReg | 120 | SMOTE | 0.667 | 0.715 | +4.75 |
| LogReg | 120 | BorderlineSMOTE | 0.667 | 0.714 | +4.62 |
| LogReg | 250 | Baseline | 0.684 | 0.684 | 0.00 |
| LogReg | 250 | ClassWeight | 0.684 | 0.724 | +4.03 |
| LogReg | 250 | RandomOver | 0.684 | 0.724 | +4.05 |
| LogReg | 250 | RandomUnder | 0.684 | 0.724 | +3.99 |
| LogReg | 250 | SMOTE | 0.684 | 0.720 | +3.68 |
| LogReg | 250 | BorderlineSMOTE | 0.684 | 0.721 | +3.72 |
| LogReg | 537 | Baseline | 0.716 | 0.716 | 0.00 |
| LogReg | 537 | ClassWeight | 0.716 | 0.734 | +1.80 |
| LogReg | 537 | RandomOver | 0.716 | 0.735 | +1.95 |
| LogReg | 537 | RandomUnder | 0.716 | 0.733 | +1.70 |
| LogReg | 537 | SMOTE | 0.716 | 0.731 | +1.56 |
| LogReg | 537 | BorderlineSMOTE | 0.716 | 0.730 | +1.37 |
| RandomForest | 60 | Baseline | 0.641 | 0.641 | 0.00 |
| RandomForest | 60 | ClassWeight | 0.641 | 0.697 | +5.59 |
| RandomForest | 60 | RandomOver | 0.641 | 0.666 | +2.52 |
| RandomForest | 60 | RandomUnder | 0.641 | 0.706 | +6.49 |
| RandomForest | 60 | SMOTE | 0.641 | 0.674 | +3.37 |
| RandomForest | 60 | BorderlineSMOTE | 0.641 | 0.670 | +2.97 |
| RandomForest | 120 | Baseline | 0.647 | 0.647 | 0.00 |
| RandomForest | 120 | ClassWeight | 0.647 | 0.693 | +4.66 |
| RandomForest | 120 | RandomOver | 0.647 | 0.671 | +2.41 |
| RandomForest | 120 | RandomUnder | 0.647 | 0.711 | +6.43 |
| RandomForest | 120 | SMOTE | 0.647 | 0.679 | +3.23 |
| RandomForest | 120 | BorderlineSMOTE | 0.647 | 0.684 | +3.69 |
| RandomForest | 250 | Baseline | 0.661 | 0.661 | 0.00 |
| RandomForest | 250 | ClassWeight | 0.661 | 0.710 | +4.91 |
| RandomForest | 250 | RandomOver | 0.661 | 0.683 | +2.21 |
| RandomForest | 250 | RandomUnder | 0.661 | 0.726 | +6.50 |
| RandomForest | 250 | SMOTE | 0.661 | 0.706 | +4.55 |
| RandomForest | 250 | BorderlineSMOTE | 0.661 | 0.697 | +3.64 |
| RandomForest | 537 | Baseline | 0.714 | 0.714 | 0.00 |
| RandomForest | 537 | ClassWeight | 0.714 | 0.740 | +2.55 |
| RandomForest | 537 | RandomOver | 0.714 | 0.728 | +1.40 |
| RandomForest | 537 | RandomUnder | 0.714 | 0.747 | +3.30 |
| RandomForest | 537 | SMOTE | 0.714 | 0.743 | +2.87 |
| RandomForest | 537 | BorderlineSMOTE | 0.714 | 0.738 | +2.41 |
