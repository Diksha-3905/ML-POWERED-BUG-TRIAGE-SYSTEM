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
        print(f"Warning: {models_dir} directory not found.")
        print("Please run 'python main.py' first to train and save the model.")
        return

    # Check if model file exists
    model_path = os.path.join(models_dir, "bug_triage_model.joblib")
    if not os.path.exists(model_path):
        print(f"Warning: Model file not found at {model_path}")
        print("Please run 'python main.py' first to train and save the model.")
        print("The API will start but predictions will not work until the model is available.")

    print("Starting Bug Triage Prediction API...")
    print("API will be available at: http://localhost:8000")
    print("API documentation will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")

    # Run the FastAPI app
    uvicorn.run(
        "api.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
