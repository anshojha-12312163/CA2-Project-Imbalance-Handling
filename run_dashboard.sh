#!/usr/bin/env bash
echo "========================================================"
echo "  CA2 Project: Imbalance-Handling Interactive Dashboard"
echo "========================================================"
echo "Installing required dependencies..."
pip install -r requirements.txt
echo ""
echo "Launching Streamlit dashboard on http://localhost:8501..."
streamlit run dashboard/app.py
