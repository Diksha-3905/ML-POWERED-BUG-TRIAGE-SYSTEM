# ML-POWERED-BUG-TRIAGE-SYSTEM
🐛 An automated bug triage system that uses NLP and Machine Learning (scikit-learn) to classify bug reports and assign them to the correct team.

# ML-Powered Bug Triage System 🐛

An automated bug triage system that uses Natural Language Processing and Machine Learning to classify bug reports and assign them to the correct team.

## 📖 Overview

In any software project, manually triaging bug reports is a time-consuming and often inconsistent process. This project aims to solve that problem by providing a simple yet effective machine learning model that reads a bug report and predicts the most relevant team for the job. This helps streamline the workflow, reduce response times, and ensure issues are handled by the right people from the start.

## ✨ Key Features

-   **Text Preprocessing:** Cleans and prepares raw bug report text for the model.
-   **TF-IDF Vectorization:** Converts text into meaningful numerical features.
-   **Model Training:** Uses a `scikit-learn` Pipeline to train a Multinomial Naive Bayes classifier.
-   **REST API:** FastAPI-powered endpoints for real-time bug triage predictions.
-   **Prediction:** Provides both CLI and API interfaces to classify new bug reports.
-   **Model Persistence:** Saves the trained model pipeline for future use.

## 🛠️ Technology Stack

-   **Python 3.10+**
-   **FastAPI:** For the REST API endpoints
-   **scikit-learn:** For the machine learning pipeline and models.
-   **Pandas:** For data manipulation and loading.
-   **NLTK:** For natural language processing tasks (e.g., stopword removal).
-   **Joblib:** For saving and loading the trained model.
-   **Uvicorn:** ASGI server for running the FastAPI application.

## 📂 Project Structure

```
ml-bug-triage/
├── api/
│   ├── api.py          # FastAPI application
│   └── ui.py           # UI components (if any)
├── data/
│   └── bugs.csv        # Training data
├── models/
│   └── bug_triage_model.joblib  # Trained model
├── main.py             # Model training script
├── predict.py          # CLI prediction script
├── run_api.py          # API startup script
├── test_api.py         # API tests
├── requirements.txt    # Dependencies
└── README.md
```

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Prerequisites

-   Python 3.10 or newer
-   pip (Python package installer)

### 2. Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/Diksha-3905/ML-POWERED-BUG-TRIAGE-SYSTEM.git
cd ML-POWERED-BUG-TRIAGE-SYSTEM
```

**2. Create and activate a virtual environment (recommended):**

-   **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
-   **macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

### 3. Usage

**1. Train the Model:**

Run the `main.py` script to process the data, train the classifier, and save the model pipeline.

```bash
python main.py
```
You should see output detailing the process, followed by a classification report evaluating the model's performance.

**2. Start the API Server:**

Run the API server to enable REST endpoints for predictions:

```bash
python run_api.py
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

**3. Make Predictions via API:**

Once the API is running, you can make predictions using HTTP requests:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Login button not working",
       "description": "Users cannot click the login button on the homepage"
     }'
```

**4. Make Predictions via CLI:**

Run the `predict.py` script to classify sample bug reports using the saved model:

```bash
python predict.py
```

## 🔌 API Endpoints

### Health Check
- **GET** `/` - Root endpoint with API status
- **GET** `/health` - Health check endpoint

### Predictions
- **POST** `/predict` - Full prediction with confidence scores and metadata
- **POST** `/predict/simple` - Simple prediction returning only the team name

### Model Information
- **GET** `/model/info` - Get information about the loaded model

### Example API Usage

**Request:**
```json
{
  "title": "Database connection timeout",
  "description": "Users are experiencing timeout errors when trying to access their data"
}
```

**Response:**
```json
{
  "predicted_team": "Backend Team",
  "confidence": 0.85,
  "preprocessed_text": "database connection timeout users experiencing timeout errors trying access data"
}
```

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
pytest test_api.py -v
```

## 📊 Model Performance

The system uses a Multinomial Naive Bayes classifier with TF-IDF vectorization. After training, you'll see a classification report showing:

- Precision, Recall, and F1-score for each team
- Overall accuracy
- Support (number of samples) for each class

## 🔧 Configuration

The API can be configured by modifying the following:

- **Model Path:** Update the model path in `api/api.py` if you store models elsewhere
- **Server Settings:** Modify host, port, and other settings in `run_api.py`
- **Preprocessing:** Adjust text preprocessing logic in `main.py`

## 📈 Future Improvements

-   ✅ **REST API:** FastAPI service for real-time predictions (Completed)
-   **Web UI:** Build a user-friendly web interface
-   **Experiment with Models:** Try more advanced models like SVM, Logistic Regression, or deep learning models (LSTM, BERT)
-   **Hyperparameter Tuning:** Use `GridSearchCV` to find the optimal parameters for the model
-   **More Data:** Integrate with real bug-tracking systems (Jira, GitHub) for larger datasets
-   **Authentication:** Add API key authentication for production use
-   **Rate Limiting:** Implement rate limiting for API endpoints
-   **Monitoring:** Add logging and monitoring capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- scikit-learn community for excellent ML tools
- FastAPI team for the amazing web framework
- NLTK contributors for natural language processing capabilities
