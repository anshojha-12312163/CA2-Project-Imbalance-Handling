@echo off
echo ========================================================
echo   CA2 Project: Imbalance-Handling Interactive Dashboard
echo ========================================================
echo Installing required dependencies...
python -m pip install -r requirements.txt
echo.
echo Launching Streamlit dashboard on http://localhost:8501...
python -m streamlit run dashboard/app.py
pause
