"""
Small + imbalanced tabular classification: Pima Indians Diabetes.
Compares imbalance-handling strategies as the TRAINING SET SIZE shrinks.

Run:  python code/run_experiments.py
Outputs -> results/ (CSV tables + PNG figures)
"""
import os, warnings
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (balanced_accuracy_score, f1_score,
                             recall_score, confusion_matrix)
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE, RandomOverSampler, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "pima_diabetes.csv")
OUT = os.path.join(ROOT, "results")
os.makedirs(OUT, exist_ok=True)

N_REPEATS = 20                        # repeated random splits
TRAIN_SIZES = [60, 120, 250, None]    # None = full training split
MINORITY_FRACTION = 0.25              # train set made more imbalanced than original (~35%)

# ---------------- data ----------------
df = pd.read_csv(DATA)
# Zero is a physiologically impossible value in these columns -> treat as missing
for c in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    df[c] = df[c].replace(0, np.nan)
X, y = df.drop(columns="Outcome").values, df["Outcome"].values


def gmean(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sens = tp / (tp + fn) if tp + fn else 0
    spec = tn / (tn + fp) if tn + fp else 0
    return np.sqrt(sens * spec)


def make_small_imbalanced(Xtr, ytr, n, frac, rng):
    """Subsample the training set to size n with minority fraction `frac`."""
    if n is None:
        return Xtr, ytr
    n_min = max(int(round(n * frac)), 6)
    n_maj = n - n_min
    idx_min = rng.choice(np.where(ytr == 1)[0], min(n_min, (ytr == 1).sum()), replace=False)
    idx_maj = rng.choice(np.where(ytr == 0)[0], min(n_maj, (ytr == 0).sum()), replace=False)
    idx = np.concatenate([idx_min, idx_maj])
    return Xtr[idx], ytr[idx]


# ---------------- methods ----------------
METHODS = ["Baseline", "ClassWeight", "RandomOver", "RandomUnder", "SMOTE", "BorderlineSMOTE"]
MODELS = ["LogReg", "RandomForest"]


def build(model_name, method, seed):
    cw = "balanced" if method == "ClassWeight" else None
    if model_name == "LogReg":
        clf = LogisticRegression(max_iter=2000, class_weight=cw)
    else:
        clf = RandomForestClassifier(n_estimators=200, class_weight=cw,
                                     random_state=seed, n_jobs=-1)
    steps = [("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]
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


# ---------------- experiments ----------------
rows = []
for rep in range(N_REPEATS):
    seed = 1000 + rep
    rng = np.random.RandomState(seed)
    Xtr_full, Xte, ytr_full, yte = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=seed)
    for n in TRAIN_SIZES:
        Xtr, ytr = make_small_imbalanced(Xtr_full, ytr_full, n, MINORITY_FRACTION, rng)
        for m in MODELS:
            for meth in METHODS:
                pipe = build(m, meth, seed).fit(Xtr, ytr)
                p = pipe.predict(Xte)
                rows.append(dict(
                    rep=rep, train_size=n if n else len(ytr_full),
                    model=m, method=meth,
                    BA=balanced_accuracy_score(yte, p),
                    F1=f1_score(yte, p, average="macro"),
                    GM=gmean(yte, p),
                    MinorityRecall=recall_score(yte, p, pos_label=1)))
    print(f"repeat {rep + 1}/{N_REPEATS} done", flush=True)

res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, "all_runs.csv"), index=False)

# ---------------- summary tables ----------------
metrics = ["BA", "F1", "GM", "MinorityRecall"]
res.groupby(["model", "train_size", "method"])[metrics].agg(["mean", "std"]).round(3) \
    .to_csv(os.path.join(OUT, "summary_mean_std.csv"))
mean_tbl = res.groupby(["model", "train_size", "method"])[metrics].mean().round(3).reset_index()
mean_tbl.to_csv(os.path.join(OUT, "summary_mean.csv"), index=False)

best = mean_tbl.loc[mean_tbl.groupby(["model", "train_size"])["BA"].idxmax()]
best.to_csv(os.path.join(OUT, "best_method_per_setting.csv"), index=False)
print("\nBest method (by Balanced Accuracy) per setting:\n", best.to_string(index=False))

# ---------------- paired Wilcoxon test vs Baseline (on BA) ----------------
stat_rows = []
for (m, n), grp in res.groupby(["model", "train_size"]):
    base = grp[grp.method == "Baseline"].sort_values("rep")["BA"].values
    for meth in METHODS[1:]:
        v = grp[grp.method == meth].sort_values("rep")["BA"].values
        try:
            p = wilcoxon(v, base).pvalue
        except ValueError:
            p = np.nan
        stat_rows.append(dict(model=m, train_size=n, method=meth,
                              mean_BA_diff=round((v - base).mean(), 4),
                              p_value=round(p, 4)))
pd.DataFrame(stat_rows).to_csv(os.path.join(OUT, "wilcoxon_vs_baseline_BA.csv"), index=False)

# ---------------- figures ----------------
for m in MODELS:
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.2))
    for ax, met in zip(axes, ["BA", "F1", "GM"]):
        for meth in METHODS:
            s = mean_tbl[(mean_tbl.model == m) & (mean_tbl.method == meth)]
            ax.plot(s.train_size, s[met], marker="o", label=meth)
        ax.set_xlabel("Training set size")
        ax.set_ylabel(met)
        ax.set_title(f"{m}: {met}")
        ax.grid(alpha=.3)
    axes[0].legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, f"fig_metrics_vs_size_{m}.png"), dpi=150)
    plt.close()

smallest = mean_tbl.train_size.min()
fig, ax = plt.subplots(figsize=(8, 4.2))
piv = mean_tbl[mean_tbl.train_size == smallest] \
    .pivot(index="method", columns="model", values="MinorityRecall").reindex(METHODS)
piv.plot(kind="bar", ax=ax)
ax.set_ylabel("Minority (diabetic) recall")
ax.set_title(f"Minority recall, training size = {smallest}")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_minority_recall_smallest.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(4.5, 3.5))
df["Outcome"].value_counts().sort_index().plot(kind="bar", ax=ax, color=["#4C72B0", "#C44E52"])
ax.set_xticklabels(["No diabetes (0)", "Diabetes (1)"], rotation=0)
ax.set_ylabel("Samples")
ax.set_title("Pima class distribution")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_class_distribution.png"), dpi=150)
plt.close()

print("\nAll results saved to", OUT)
