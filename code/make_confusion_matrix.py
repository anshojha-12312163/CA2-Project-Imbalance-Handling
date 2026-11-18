"""
code/make_confusion_matrix.py

1. Reads results/best_method_per_setting.csv to identify the best method
   by Balanced Accuracy for each model (LogReg, RandomForest) on the full
   training size (N = 537).
2. Retrains each optimal pipeline on one stratified 70/30 train/test split
   (random_state = 1000), using the exact preprocessing and resampling
   inside an imblearn Pipeline as run_experiments.py.
3. Saves a high-quality confusion matrix visualization for each model to:
   - results/fig_confusion_matrix_LogReg.png
   - results/fig_confusion_matrix_RandomForest.png
   with labels "No diabetes" and "Diabetes" and exact counts displayed.

Usage:
    python code/make_confusion_matrix.py
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, balanced_accuracy_score, recall_score
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE, RandomOverSampler, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler

warnings.filterwarnings("ignore")

# ----------------- PATH SETUP -----------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(CURRENT_DIR, "..", "data", "pima_diabetes.csv")):
    ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
elif os.path.exists(os.path.join(CURRENT_DIR, "..", "project", "data", "pima_diabetes.csv")):
    ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "project"))
elif os.path.exists(os.path.join(CURRENT_DIR, "data", "pima_diabetes.csv")):
    ROOT = CURRENT_DIR
else:
    ROOT = os.getcwd()

DATA_PATH = os.path.join(ROOT, "data", "pima_diabetes.csv")
BEST_CSV_PATH = os.path.join(ROOT, "results", "best_method_per_setting.csv")
OUT_DIR = os.path.join(ROOT, "results")
os.makedirs(OUT_DIR, exist_ok=True)

SEED = 1000


def get_best_methods_full_size():
    """
    Reads best_method_per_setting.csv and finds the best method
    for full training size (N = 537) for each model.
    """
    if not os.path.exists(BEST_CSV_PATH):
        raise FileNotFoundError(f"Missing best methods file: {BEST_CSV_PATH}")

    df_best = pd.read_csv(BEST_CSV_PATH)
    full_size = df_best["train_size"].max()
    sub = df_best[df_best["train_size"] == full_size]

    best_methods = {}
    for _, row in sub.iterrows():
        best_methods[row["model"]] = {
            "method": row["method"],
            "train_size": row["train_size"],
            "BA": row["BA"],
        }
    return best_methods


def build_pipeline(model_name, method, seed):
    """
    Builds the imblearn Pipeline ensuring resampling is performed
    strictly inside the pipeline during fit() to prevent data leakage.
    """
    cw = "balanced" if method == "ClassWeight" else None
    if model_name == "LogReg":
        clf = LogisticRegression(max_iter=2000, class_weight=cw, random_state=seed)
    else:
        clf = RandomForestClassifier(n_estimators=200, class_weight=cw,
                                     random_state=seed, n_jobs=-1)

    steps = [
        ("imp", SimpleImputer(strategy="median")),
        ("sc", StandardScaler()),
    ]

    if method == "RandomOver":
        steps.append(("s", RandomOverSampler(random_state=seed)))
    elif method == "RandomUnder":
        steps.append(("s", RandomUnderSampler(random_state=seed)))
    elif method == "SMOTE":
        steps.append(("s", SMOTE(k_neighbors=3, random_state=seed)))
    elif method == "BorderlineSMOTE":
        steps.append(("s", BorderlineSMOTE(k_neighbors=3, random_state=seed)))

    steps.append(("clf", clf))
    return Pipeline(steps)


def plot_and_save_confusion_matrix(y_true, y_pred, model_name, method_name, out_path):
    """
    Plots confusion matrix with labels 'No diabetes' and 'Diabetes'
    and sample counts clearly displayed.
    """
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    ba = balanced_accuracy_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred, pos_label=1)
    spec = tn / (tn + fp) if (tn + fp) else 0

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["No diabetes", "Diabetes"],
    )
    disp.plot(ax=ax, cmap="Blues", values_format="d", colorbar=True)

    # Styling
    model_title = "Logistic Regression" if model_name == "LogReg" else "Random Forest"
    ax.set_title(
        f"{model_title} ({method_name}) Confusion Matrix\n"
        f"Test BA: {ba:.3f} | Minority Recall (Sens): {rec:.3f} | Specificity: {spec:.3f}",
        fontsize=11,
        pad=14,
        weight="bold",
    )
    ax.set_xlabel("Predicted Label", fontsize=11, labelpad=8)
    ax.set_ylabel("True Label", fontsize=11, labelpad=8)

    # Text styling inside cells
    for text in disp.text_.ravel():
        text.set_fontsize(13)
        text.set_fontweight("bold")

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved confusion matrix figure to: {out_path}")
    print(f"  {model_name} ({method_name}) -> TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp} (BA: {ba:.3f})")


def main():
    print(f"Loading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    # Treat physiologically impossible zeros as NaN (matching run_experiments.py)
    for c in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
        df[c] = df[c].replace(0, np.nan)

    X = df.drop(columns="Outcome").values
    y = df["Outcome"].values

    # Determine best methods on full training size
    best_methods = get_best_methods_full_size()
    print("\nBest methods for full training size (N = 537):")
    for m, info in best_methods.items():
        print(f"  - {m}: {info['method']} (Cross-run Mean BA: {info['BA']:.3f})")

    # One stratified 70/30 train/test split with seed 1000
    Xtr_full, Xte, ytr_full, yte = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=SEED
    )

    print(f"\nRetraining optimal pipelines on split seed = {SEED}...")
    for model_name in ["LogReg", "RandomForest"]:
        if model_name not in best_methods:
            continue
        method = best_methods[model_name]["method"]
        print(f"\nTraining {model_name} with best method '{method}'...")

        pipe = build_pipeline(model_name, method, SEED)
        pipe.fit(Xtr_full, ytr_full)
        y_pred = pipe.predict(Xte)

        fig_path = os.path.join(OUT_DIR, f"fig_confusion_matrix_{model_name}.png")
        plot_and_save_confusion_matrix(yte, y_pred, model_name, method, fig_path)

    print("\nTask 2 completed successfully.")


if __name__ == "__main__":
    main()
