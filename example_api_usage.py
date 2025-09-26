#!/usr/bin/env python3
"""
Example script demonstrating how to use the Bug Triage Prediction API
"""

import json
import time

import requests

# API base URL
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if the API is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API Status: {health_data['status']}")
            print(f"✅ Model Loaded: {health_data['model_loaded']}")
            return health_data['model_loaded']
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def get_model_info():
    """Get information about the loaded model"""
    try:
        response = requests.get(f"{API_BASE_URL}/model/info")
        if response.status_code == 200:
            model_info = response.json()
            print("\n📊 Model Information:")
            print(f"   Model Type: {model_info.get('model_type', 'Unknown')}")
            if 'classes' in model_info:
                print(f"   Available Teams: {', '.join(model_info['classes'])}")
            if 'vocabulary_size' in model_info:
                print(f"   Vocabulary Size: {model_info['vocabulary_size']}")
            return model_info
        else:
            print(f"❌ Failed to get model info: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting model info: {e}")
        return None

def predict_bug_team(title, description, use_simple=False):
    """Make a prediction for a bug report"""
    endpoint = "/predict/simple" if use_simple else "/predict"

    bug_report = {
        "title": title,
        "description": description
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=bug_report,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.json().get('detail', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error making prediction: {e}")
        return None

def main():
    """Main function demonstrating API usage"""
    print("🐛 Bug Triage Prediction API Example")
    print("=" * 40)

    # Check API health
    if not check_api_health():
        print("\n❌ API is not available. Please start the server first:")
        print("   python run_api.py")
        return

    # Get model information
    get_model_info()

    # Example bug reports
    bug_reports = [
        {
            "title": "Login button not responding",
            "description": "Users are unable to click the login button on the homepage. The button appears to be disabled even when all fields are filled correctly."
        },
        {
            "title": "Database connection timeout",
            "description": "The application is throwing timeout errors when trying to connect to the database. This happens intermittently during peak hours."
        },
        {
            "title": "Mobile app crashes on iOS",
            "description": "The mobile application crashes immediately after opening on iOS devices running version 16.0 and above. Android version works fine."
        },
        {
            "title": "API returning 500 error",
            "description": "The /api/users endpoint is returning internal server error 500 when trying to fetch user data. The error logs show a null pointer exception."
        }
    ]

    print("\n🔮 Making Predictions:")
    print("=" * 40)

    for i, bug in enumerate(bug_reports, 1):
        print(f"\n📝 Bug Report #{i}:")
        print(f"   Title: {bug['title']}")
        print(f"   Description: {bug['description'][:100]}...")

        # Make detailed prediction
        result = predict_bug_team(bug['title'], bug['description'])

        if result:
            print(f"   🎯 Predicted Team: {result['predicted_team']}")
            if 'confidence' in result and result['confidence']:
                print(f"   📊 Confidence: {result['confidence']:.2%}")

        # Small delay between requests
        time.sleep(0.5)

    print("\n✨ Example completed!")
    print("\nTo start the API server, run: python run_api.py")
    print("To view interactive docs, visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
