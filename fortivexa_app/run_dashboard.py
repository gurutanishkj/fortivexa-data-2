"""
Convenient launcher for FORTIVEXA Streamlit Command Center
"""
import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dashboard_path = os.path.join(BASE_DIR, "ui", "dashboard.py")

if __name__ == "__main__":
    print("[Starting FORTIVEXA Streamlit Command Center on 0.0.0.0:8501 (Host Server Mode)]...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", dashboard_path,
        "--server.address", "0.0.0.0",
        "--server.port", "8501",
        "--server.headless", "true"
    ])
