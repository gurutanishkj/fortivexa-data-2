"""
Convenient launcher for FORTIVEXA Streamlit Command Center
"""
import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dashboard_path = os.path.join(BASE_DIR, "ui", "dashboard.py")

if __name__ == "__main__":
    print("[Starting FORTIVEXA Streamlit Command Center on http://localhost:8501]...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
