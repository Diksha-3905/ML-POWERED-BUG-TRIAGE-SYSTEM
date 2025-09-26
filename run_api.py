#!/usr/bin/env python3
"""
Startup script for the Bug Triage Prediction API
"""
import os
import sys
import uvicorn

def main():
    """Run the FastAPI application"""
    # Ensure the models directory exists
    models_dir = "models"
    if not os.path.exists(models_dir):
        print(f"Warning: {models_dir} directory not found. Please run main.py first to train the model.")

    # Check if model file exists
    model_path = os.path.join(models_dir, "bug_triage_model.joblib")
    if not os.path.exists(model_path):
        print(f"Warning: Model file not found at {model_path}. Please run main.py first to train the model.")

    # Run the API
    uvicorn.run("api.api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
