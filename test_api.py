import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.api import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_model():
    """Create a mock model for testing"""
    mock = MagicMock()
    mock.predict.return_value = ["Frontend Team"]
    mock.predict_proba.return_value = [[0.1, 0.8, 0.1]]
    mock.named_steps = {
        'tfidf': MagicMock(),
        'classifier': MagicMock()
    }
    mock.named_steps['tfidf'].vocabulary_ = {'test': 0, 'bug': 1}
    mock.named_steps['tfidf'].ngram_range = (1, 2)
    mock.named_steps['classifier'].classes_ = ['Frontend Team', 'Backend Team', 'DevOps Team']
    return mock


@pytest.fixture
def sample_bug_report():
    """Sample bug report for testing"""
    return {
        "title": "Login button not working",
        "description": "When users click the login button, nothing happens. The page doesn't redirect and no error message is shown."
    }


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns health status"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "message" in data

    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "message" in data


class TestPredictionEndpoints:
    """Test prediction endpoints"""

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_predict_endpoint_success(self, mock_model_var, client, sample_bug_report, mock_model):
        """Test successful prediction"""
        mock_model_var = mock_model

        response = client.post("/predict", json=sample_bug_report)
        assert response.status_code == 200

        data = response.json()
        assert "predicted_team" in data
        assert "confidence" in data
        assert "preprocessed_text" in data
        assert data["predicted_team"] == "Frontend Team"

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_predict_simple_endpoint_success(self, mock_model_var, client, sample_bug_report, mock_model):
        """Test successful simple prediction"""
        mock_model_var = mock_model

        response = client.post("/predict/simple", json=sample_bug_report)
        assert response.status_code == 200

        data = response.json()
        assert "predicted_team" in data
        assert data["predicted_team"] == "Frontend Team"

    @patch('api.api.model_loaded', False)
    def test_predict_endpoint_model_not_loaded(self, client, sample_bug_report):
        """Test prediction when model is not loaded"""
        response = client.post("/predict", json=sample_bug_report)
        assert response.status_code == 503
        assert "Model not available" in response.json()["detail"]

    def test_predict_endpoint_invalid_input(self, client):
        """Test prediction with invalid input"""
        invalid_report = {"title": "", "description": ""}
        response = client.post("/predict", json=invalid_report)
        assert response.status_code == 422  # Validation error

    def test_predict_endpoint_missing_fields(self, client):
        """Test prediction with missing required fields"""
        incomplete_report = {"title": "Test bug"}
        response = client.post("/predict", json=incomplete_report)
        assert response.status_code == 422  # Validation error

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_predict_endpoint_empty_preprocessed_text(self, mock_model_var, client, mock_model):
        """Test prediction when preprocessed text is empty"""
        mock_model_var = mock_model

        # Bug report with only special characters and stopwords
        empty_content_report = {
            "title": "!@#$%",
            "description": "the and or but"
        }

        response = client.post("/predict", json=empty_content_report)
        assert response.status_code == 400
        assert "Preprocessed text is empty" in response.json()["detail"]


class TestModelInfoEndpoint:
    """Test model info endpoint"""

    @patch('api.api.model')
    @patch('api.api.model_loaded', True)
    def test_model_info_success(self, mock_model_var, client, mock_model):
        """Test successful model info retrieval"""
        mock_model_var = mock_model

        response = client.get("/model/info")
        assert response.status_code == 200

        data = response.json()
        assert "model_type" in data
        assert "model_loaded" in data
        assert data["model_loaded"] is True

    @patch('api.api.model_loaded', False)
    def test_model_info_model_not_loaded(self, client):
        """Test model info when model is not loaded"""
        response = client.get("/model/info")
        assert response.status_code == 503
        assert "Model not available" in response.json()["detail"]
