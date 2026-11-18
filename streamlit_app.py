"""
Streamlit Community Cloud root entrypoint.
Seamlessly routes execution to the clinical benchmark dashboard in dashboard/app.py.
"""
import os
import sys

# Ensure root directory is in Python module search path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dashboard.app import main

if __name__ == "__main__":
    main()
