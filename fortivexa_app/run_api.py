"""
Convenient launcher for FORTIVEXA FastAPI REST Microservice
"""
import os
import sys
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    print("[Starting FORTIVEXA FastAPI Service on 0.0.0.0:8000 (Host Server Mode)]...")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
