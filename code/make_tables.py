"""
code/make_tables.py

Reads results/all_runs.csv and generates formatted comparison tables:
1. Mean ± Std (over 20 repeated runs) for:
   - Macro F1
   - Balanced Accuracy
   - G-mean
   - Minority Recall
   for each model (LogReg, RandomForest) and training size (60, 120, 250, 537),
   with the best mean bolded in each column.
2. Gain in Balanced Accuracy over Baseline in percentage points (pp) for every
   model, training size, and method.

Outputs:
- results/paper_tables.md (Markdown format)
- results/paper_tables.xlsx (Excel format with one sheet per model)

Usage:
    python code/make_tables.py
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ----------------- PATH SETUP -----------------
# Dynamically locate ROOT so the script works whether run from project root,
# project/code, or CA2_Project root.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(CURRENT_DIR, "..", "results", "all_runs.csv")):
    ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
elif os.path.exists(os.path.join(CURRENT_DIR, "..", "project", "results", "all_runs.csv")):
    ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "project"))
elif os.path.exists(os.path.join(CURRENT_DIR, "results", "all_runs.csv")):
    ROOT = CURRENT_DIR
else:
    ROOT = os.getcwd()

ALL_RUNS_CSV = os.path.join(ROOT, "results", "all_runs.csv")
MD_OUT = os.path.join(ROOT, "results", "paper_tables.md")
XLSX_OUT = os.path.join(ROOT, "results", "paper_tables.xlsx")

# ----------------- CONSTANTS -----------------
METHODS = [
    "Baseline",
    "ClassWeight",
    "RandomOver",
    "RandomUnder",
    "SMOTE",
    "BorderlineSMOTE",
]
MODELS = ["LogReg", "RandomForest"]
TRAIN_SIZES = [60, 120, 250, 537]
METRICS = [
    ("F1", "Macro F1"),
    ("BA", "Balanced Accuracy"),
    ("GM", "G-mean"),
    ("MinorityRecall", "Minority Recall"),
]


def load_data():
    if not os.path.exists(ALL_RUNS_CSV):
        raise FileNotFoundError(f"Could not find results file at: {ALL_RUNS_CSV}")
    return pd.read_csv(ALL_RUNS_CSV)


def compute_summary_tables(df):
    """
    Computes mean and std for each model, size, and method across runs.
    Returns nested structure:
    tables[model][size] = {
        'data': DataFrame with methods as rows,
        'best_methods': {metric_col: best_method_name}
    }
    """
    tables = {m: {} for m in MODELS}

    for m in MODELS:
        for sz in TRAIN_SIZES:
            sub = df[(df.model == m) & (df.train_size == sz)]
            rows = []
            best_methods = {}

            # First compute mean and std for each method
            stats = {}
            for meth in METHODS:
                meth_sub = sub[sub.method == meth]
                stats[meth] = {}
                for m_col, _ in METRICS:
                    val_mean = meth_sub[m_col].mean()
                    val_std = meth_sub[m_col].std(ddof=1)
                    stats[meth][m_col] = (val_mean, val_std)

            # Determine best method per metric (maximum mean)
            for m_col, _ in METRICS:
                best_meth = max(METHODS, key=lambda meth: stats[meth][m_col][0])
                best_methods[m_col] = best_meth

            # Build row dicts
            for meth in METHODS:
                row_dict = {"Method": meth}
                for m_col, m_display in METRICS:
                    mean_val, std_val = stats[meth][m_col]
                    row_dict[m_display] = {
                        "mean": mean_val,
                        "std": std_val,
                        "formatted": f"{mean_val:.3f} ± {std_val:.3f}",
                        "is_best": (meth == best_methods[m_col]),
                    }
                rows.append(row_dict)

            tables[m][sz] = {
                "rows": rows,
                "best_methods": best_methods,
                "stats": stats,
            }

    return tables


def compute_ba_gain_table(df):
    """
    Computes gain in Balanced Accuracy over Baseline in percentage points (pp)
    for every model, training size, and method:
    gain_pp = (mean_BA(method) - mean_BA(Baseline)) * 100
    """
    gain_records = []
    matrix_per_model = {m: {} for m in MODELS}

    for m in MODELS:
        for sz in TRAIN_SIZES:
            sub = df[(df.model == m) & (df.train_size == sz)]
            base_mean_ba = sub[sub.method == "Baseline"]["BA"].mean()

            for meth in METHODS:
                meth_sub = sub[sub.method == meth]
                meth_mean_ba = meth_sub["BA"].mean()
                gain_pp = (meth_mean_ba - base_mean_ba) * 100

                gain_records.append({
                    "Model": m,
                    "Training Size": sz,
                    "Method": meth,
                    "Baseline BA": base_mean_ba,
                    "Method BA": meth_mean_ba,
                    "Gain (pp)": gain_pp,
                })

                if meth not in matrix_per_model[m]:
                    matrix_per_model[m][meth] = {}
                matrix_per_model[m][meth][sz] = {
                    "gain_pp": gain_pp,
                    "method_ba": meth_mean_ba,
                    "base_ba": base_mean_ba,
                }

    return pd.DataFrame(gain_records), matrix_per_model


def generate_markdown(tables, gain_df, gain_matrix):
    """
    Builds the complete Markdown text for paper_tables.md.
    """
    lines = []
    lines.append("# Experimental Results & Performance Tables")
    lines.append("")
    lines.append("This document contains evaluation tables generated from `results/all_runs.csv` over 20 repeated Monte Carlo stratified 70/30 splits.")
    lines.append("Values are displayed as **Mean ± Standard Deviation**. The best performing mean in each column is highlighted in **bold**.")
    lines.append("")

    for m in MODELS:
        model_name = "Logistic Regression (LogReg)" if m == "LogReg" else "Random Forest (RandomForest)"
        lines.append(f"## Model: {model_name}")
        lines.append("")

        for sz in TRAIN_SIZES:
            size_label = f"N = {sz}" if sz != 537 else f"N = 537 (Full Training Set)"
            lines.append(f"### Table: {m} - Training Size: {size_label}")
            lines.append("")
            lines.append("| Method | Macro F1 | Balanced Accuracy | G-mean | Minority Recall |")
            lines.append("| :--- | :---: | :---: | :---: | :---: |")

            table_info = tables[m][sz]
            for row in table_info["rows"]:
                meth = row["Method"]
                cols = []
                for _, m_display in METRICS:
                    cell_data = row[m_display]
                    text = cell_data["formatted"]
                    if cell_data["is_best"]:
                        cols.append(f"**{text}**")
                    else:
                        cols.append(text)
                lines.append(f"| {meth} | {cols[0]} | {cols[1]} | {cols[2]} | {cols[3]} |")
            lines.append("")

        # BA Gain table for this model
        lines.append(f"### Balanced Accuracy Gain over Baseline (percentage points) - {m}")
        lines.append("")
        lines.append("| Method | N = 60 (pp) | N = 120 (pp) | N = 250 (pp) | Full (N = 537) (pp) |")
        lines.append("| :--- | :---: | :---: | :---: | :---: |")

        # Find best gain per size column
        best_gains = {}
        for sz in TRAIN_SIZES:
            best_gains[sz] = max(gain_matrix[m][meth][sz]["gain_pp"] for meth in METHODS)

        for meth in METHODS:
            cols = []
            for sz in TRAIN_SIZES:
                gain_val = gain_matrix[m][meth][sz]["gain_pp"]
                if meth == "Baseline":
                    text = "0.00"
                else:
                    text = f"{gain_val:+.2f}"
                if gain_val == best_gains[sz] and meth != "Baseline":
                    cols.append(f"**{text}**")
                else:
                    cols.append(text)
            lines.append(f"| {meth} | {cols[0]} | {cols[1]} | {cols[2]} | {cols[3]} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Overall Summary Table of Balanced Accuracy Gain across all models and sizes
    lines.append("## Overall Summary: Gain in Balanced Accuracy over Baseline")
    lines.append("")
    lines.append("| Model | Training Size | Method | Baseline Mean BA | Method Mean BA | Gain (pp) |")
    lines.append("| :--- | :---: | :--- | :---: | :---: | :---: |")

    for _, row in gain_df.iterrows():
        gain_str = f"{row['Gain (pp)']:+.2f}" if row['Method'] != 'Baseline' else "0.00"
        lines.append(
            f"| {row['Model']} | {row['Training Size']} | {row['Method']} | "
            f"{row['Baseline BA']:.3f} | {row['Method BA']:.3f} | {gain_str} |"
        )
    lines.append("")

    return "\n".join(lines)


def generate_excel(tables, gain_matrix):
    """
    Saves an Excel workbook with one sheet per model, containing:
    1. Performance tables (mean ± std) for each training size with best values bolded.
    2. Gain in Balanced Accuracy over Baseline (pp) table.
    """
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    font_title = Font(name="Calibri", size=14, bold=True, color="1F497D")
    font_section = Font(name="Calibri", size=11, bold=True, color="262626")
    font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_regular = Font(name="Calibri", size=10, bold=False)
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_subnote = Font(name="Calibri", size=9, italic=True, color="595959")

    fill_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    fill_gain_header = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    fill_best = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    fill_zebra = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    thin_border_side = Side(style="thin", color="D9D9D9")
    border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")

    for m in MODELS:
        ws = wb.create_sheet(title=m)
        ws.views.sheetView[0].showGridLines = True

        current_row = 1
        model_display = "Logistic Regression (LogReg)" if m == "LogReg" else "Random Forest (RandomForest)"

        # Sheet Title
        ws.cell(row=current_row, column=1, value=f"{model_display} - Performance Summary (Mean ± Std over 20 Runs)").font = font_title
        current_row += 1
        ws.cell(row=current_row, column=1, value="Note: Values are Mean ± Std. Best mean values per metric column are bolded.").font = font_subnote
        current_row += 2

        # Tables per training size
        for sz in TRAIN_SIZES:
            size_label = f"Training Set Size: N = {sz}" if sz != 537 else "Full Training Set Size: N = 537"
            ws.cell(row=current_row, column=1, value=size_label).font = font_section
            current_row += 1

            # Headers
            headers = ["Method", "Macro F1", "Balanced Accuracy", "G-mean", "Minority Recall"]
            for col_idx, h_text in enumerate(headers, start=1):
                cell = ws.cell(row=current_row, column=col_idx, value=h_text)
                cell.font = font_header
                cell.fill = fill_header
                cell.alignment = align_center if col_idx > 1 else align_left
                cell.border = border_cell
            current_row += 1

            # Rows
            table_info = tables[m][sz]
            for r_idx, row in enumerate(table_info["rows"]):
                # Method column
                c_meth = ws.cell(row=current_row, column=1, value=row["Method"])
                c_meth.font = font_regular
                c_meth.alignment = align_left
                c_meth.border = border_cell
                if r_idx % 2 == 1:
                    c_meth.fill = fill_zebra

                for col_idx, (_, m_display) in enumerate(METRICS, start=2):
                    cell_data = row[m_display]
                    cell = ws.cell(row=current_row, column=col_idx, value=cell_data["formatted"])
                    cell.alignment = align_center
                    cell.border = border_cell
                    if cell_data["is_best"]:
                        cell.font = font_bold
                        cell.fill = fill_best
                    else:
                        cell.font = font_regular
                        if r_idx % 2 == 1:
                            cell.fill = fill_zebra
                current_row += 1

            current_row += 2  # Blank rows between tables

        # Section: Gain in Balanced Accuracy over Baseline
        ws.cell(row=current_row, column=1, value="Gain in Balanced Accuracy over Baseline (Percentage Points, pp)").font = font_section
        current_row += 1

        gain_headers = ["Method", "N = 60 (pp)", "N = 120 (pp)", "N = 250 (pp)", "Full (N = 537) (pp)"]
        for col_idx, gh in enumerate(gain_headers, start=1):
            cell = ws.cell(row=current_row, column=col_idx, value=gh)
            cell.font = font_header
            cell.fill = fill_gain_header
            cell.alignment = align_center if col_idx > 1 else align_left
            cell.border = border_cell
        current_row += 1

        # Determine best gain per size
        best_gains = {}
        for sz in TRAIN_SIZES:
            best_gains[sz] = max(gain_matrix[m][meth][sz]["gain_pp"] for meth in METHODS)

        for r_idx, meth in enumerate(METHODS):
            c_meth = ws.cell(row=current_row, column=1, value=meth)
            c_meth.font = font_regular
            c_meth.alignment = align_left
            c_meth.border = border_cell
            if r_idx % 2 == 1:
                c_meth.fill = fill_zebra

            for col_idx, sz in enumerate(TRAIN_SIZES, start=2):
                gain_val = gain_matrix[m][meth][sz]["gain_pp"]
                cell_val = "0.00" if meth == "Baseline" else f"{gain_val:+.2f}"
                cell = ws.cell(row=current_row, column=col_idx, value=cell_val)
                cell.alignment = align_center
                cell.border = border_cell
                if gain_val == best_gains[sz] and meth != "Baseline":
                    cell.font = font_bold
                    cell.fill = fill_best
                else:
                    cell.font = font_regular
                    if r_idx % 2 == 1:
                        cell.fill = fill_zebra

            current_row += 1

        # Adjust column widths automatically
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                # Ignore very long title rows for column width calculation
                if cell.row in [1, 2]:
                    continue
                max_len = max(max_len, len(val))
            ws.column_dimensions[col_letter].width = max(max_len + 5, 14)

    wb.save(XLSX_OUT)


def main():
    print(f"Reading experimental data from: {ALL_RUNS_CSV}")
    df = load_data()

    print("Computing mean ± std performance tables...")
    tables = compute_summary_tables(df)

    print("Computing Balanced Accuracy gain tables...")
    gain_df, gain_matrix = compute_ba_gain_table(df)

    print(f"Writing Markdown tables to: {MD_OUT}")
    md_content = generate_markdown(tables, gain_df, gain_matrix)
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Writing Excel workbook to: {XLSX_OUT}")
    generate_excel(tables, gain_matrix)

    print("Task 1 completed successfully.")


if __name__ == "__main__":
    main()
