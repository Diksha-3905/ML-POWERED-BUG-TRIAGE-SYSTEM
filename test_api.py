import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.api import app

client = TestClient(app)

class TestBugTriageAPI:
    """Test suite for the Bug Triage Prediction API"""

    def test_root_endpoint(self):
        """Test the root endpoint returns health status"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "message" in data

    def test_health_check_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "message" in data

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_predict_endpoint_success(self, mock_model):
        """Test successful prediction"""
        # Mock model prediction
        mock_model.predict.return_value = ["Frontend Team"]
        mock_model.predict_proba.return_value = [[0.1, 0.8, 0.1]]

        bug_report = {
            "title": "Button not working on login page",
            "description": "The submit button on the login page is not responding to clicks"
        }

        response = client.post("/predict", json=bug_report)
        assert response.status_code == 200

        data = response.json()
        assert data["predicted_team"] == "Frontend Team"
        assert "confidence" in data
        assert "preprocessed_text" in data

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_predict_simple_endpoint_success(self, mock_model):
        """Test successful simple prediction"""
        # Mock model prediction
        mock_model.predict.return_value = ["Backend Team"]

        bug_report = {
            "title": "Database connection timeout",
            "description": "Users are experiencing timeout errors when trying to access their data"
        }

        response = client.post("/predict/simple", json=bug_report)
        assert response.status_code == 200

        data = response.json()
        assert data["predicted_team"] == "Backend Team"

    def test_predict_endpoint_invalid_input(self):
        """Test prediction with invalid input"""
        # Missing required fields
        response = client.post("/predict", json={})
        assert response.status_code == 422

        # Empty strings
        bug_report = {
            "title": "",
            "description": ""
        }
        response = client.post("/predict", json=bug_report)
        assert response.status_code == 422

    @patch('api.api.model_loaded', False)
    def test_predict_endpoint_model_not_loaded(self):
        """Test prediction when model is not loaded"""
        bug_report = {
            "title": "Test bug",
            "description": "Test description"
        }

        response = client.post("/predict", json=bug_report)
        assert response.status_code == 503
        assert "Model not available" in response.json()["detail"]

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_predict_endpoint_model_error(self, mock_model):
        """Test prediction when model throws an error"""
        # Mock model to raise an exception
        mock_model.predict.side_effect = Exception("Model prediction failed")

        bug_report = {
            "title": "Test bug",
            "description": "Test description"
        }

        response = client.post("/predict", json=bug_report)
        assert response.status_code == 500
        assert "Prediction failed" in response.json()["detail"]

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_model_info_endpoint(self, mock_model):
        """Test model info endpoint"""
        # Mock model with pipeline structure
        mock_model.__class__.__name__ = "Pipeline"
        mock_model.named_steps = {
            'tfidf': MagicMock(),
            'classifier': MagicMock()
        }
        mock_model.named_steps['tfidf'].vocabulary_ = {'test': 1, 'word': 2}
        mock_model.named_steps['tfidf'].ngram_range = (1, 2)
        mock_model.named_steps['classifier'].classes_ = ['Team A', 'Team B']

        response = client.get("/model/info")
        assert response.status_code == 200

        data = response.json()
        assert data["model_type"] == "Pipeline"
        assert data["model_loaded"] is True
        assert "pipeline_steps" in data
        assert "vocabulary_size" in data
        assert "ngram_range" in data
        assert "classes" in data

    @patch('api.api.model_loaded', False)
    def test_model_info_endpoint_no_model(self):
        """Test model info endpoint when model is not loaded"""
        response = client.get("/model/info")
        assert response.status_code == 503
        assert "Model not available" in response.json()["detail"]

    def test_request_validation(self):
        """Test request validation for various edge cases"""
        # Title too long
        long_title = "x" * 501
        bug_report = {
            "title": long_title,
            "description": "Valid description"
        }
        response = client.post("/predict", json=bug_report)
        assert response.status_code == 422

        # Description too long
        long_description = "x" * 5001
        bug_report = {
            "title": "Valid title",
            "description": long_description
        }
        response = client.post("/predict", json=bug_report)
        assert response.status_code == 422

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_preprocessing_edge_cases(self, mock_model):
        """Test preprocessing with edge cases"""
        mock_model.predict.return_value = ["Test Team"]

        # Special characters and numbers
        bug_report = {
            "title": "Bug #123 with $pecial ch@racters!",
            "description": "Error 404 when accessing /api/v1/users endpoint"
        }

        response = client.post("/predict", json=bug_report)
        assert response.status_code == 200

        data = response.json()
        # Check that preprocessing removed special characters
        assert "#" not in data["preprocessed_text"]
        assert "$" not in data["preprocessed_text"]
        assert "@" not in data["preprocessed_text"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
