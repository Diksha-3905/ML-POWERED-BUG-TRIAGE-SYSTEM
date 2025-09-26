import os
import sys
from typing import Optional

import joblib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Add parent directory to path to import from main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import preprocess_text
except ImportError:
    # Fallback preprocessing function if main.py is not available
    import re

    import nltk
    from nltk.corpus import stopwords

    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')

    def preprocess_text(text):
        """
        Cleans and preprocesses a single text string.
        """
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = text.split()
        filtered_words = [word for word in words if word not in stop_words]
        return ' '.join(filtered_words)

app = FastAPI(
    title="Bug Triage Prediction API",
    description="ML-powered API for predicting the appropriate team assignment for bug reports",
    version="1.0.0"
)

# Pydantic models for request/response
class BugReport(BaseModel):
    title: str = Field(..., description="Bug report title", min_length=1, max_length=500)
    description: str = Field(..., description="Bug report description", min_length=1, max_length=5000)

class PredictionResponse(BaseModel):
    predicted_team: str = Field(..., description="Predicted team for the bug report")
    confidence: Optional[float] = Field(None, description="Prediction confidence score")
    preprocessed_text: Optional[str] = Field(None, description="Preprocessed text used for prediction")

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    message: str

# Global variable to store the loaded model
model = None

def load_model():
    """Load the trained model from disk"""
    global model
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'bug_triage_model.joblib')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        model = joblib.load(model_path)
        return True
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")

# Load model on startup
try:
    load_model()
    model_loaded = True
    startup_message = "Model loaded successfully"
except Exception as e:
    model_loaded = False
    startup_message = f"Failed to load model: {str(e)}"

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint providing API health status"""
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        message=startup_message
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        message="Model is ready for predictions" if model_loaded else "Model not loaded"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_bug_team(bug_report: BugReport):
    """
    Predict the appropriate team for a bug report

    Args:
        bug_report: BugReport object containing title and description

    Returns:
        PredictionResponse with predicted team and additional metadata
    """
    if not model_loaded or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not available. Please ensure the model is trained and saved."
        )

    try:
        # Combine title and description
        bug_text = f"{bug_report.title} {bug_report.description}"

        # Preprocess the text
        clean_bug_text = preprocess_text(bug_text)

        if not clean_bug_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Preprocessed text is empty. Please provide meaningful title and description."
            )

        # Make prediction
        prediction = model.predict([clean_bug_text])
        predicted_team = prediction[0]

        # Get prediction probabilities for confidence score
        try:
            prediction_proba = model.predict_proba([clean_bug_text])
            confidence = float(max(prediction_proba[0]))
        except AttributeError:
            # Some models don't support predict_proba
            confidence = None

        return PredictionResponse(
            predicted_team=predicted_team,
            confidence=confidence,
            preprocessed_text=clean_bug_text
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.post("/predict/simple")
async def predict_bug_team_simple(bug_report: BugReport):
    """
    Simple prediction endpoint that returns only the team name

    Args:
        bug_report: BugReport object containing title and description

    Returns:
        Dictionary with predicted team
    """
    if not model_loaded or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not available. Please ensure the model is trained and saved."
        )

    try:
        # Combine title and description
        bug_text = f"{bug_report.title} {bug_report.description}"

        # Preprocess the text
        clean_bug_text = preprocess_text(bug_text)

        if not clean_bug_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Preprocessed text is empty. Please provide meaningful title and description."
            )

        # Make prediction
        prediction = model.predict([clean_bug_text])

        return {"predicted_team": prediction[0]}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/model/info")
async def get_model_info():
    """Get information about the loaded model"""
    if not model_loaded or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not available"
        )

    try:
        model_info = {
            "model_type": type(model).__name__,
            "model_loaded": True
        }

        # Try to get additional info if it's a pipeline
        if hasattr(model, 'named_steps'):
            model_info["pipeline_steps"] = list(model.named_steps.keys())

            # Get vectorizer info if available
            if 'tfidf' in model.named_steps:
                vectorizer = model.named_steps['tfidf']
                if hasattr(vectorizer, 'vocabulary_'):
                    model_info["vocabulary_size"] = len(vectorizer.vocabulary_)
                if hasattr(vectorizer, 'ngram_range'):
                    model_info["ngram_range"] = vectorizer.ngram_range

            # Get classifier info if available
            if 'classifier' in model.named_steps:
                classifier = model.named_steps['classifier']
                if hasattr(classifier, 'classes_'):
                    model_info["classes"] = classifier.classes_.tolist()

        return model_info

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model info: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
