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
-   **Prediction:** Provides a simple script to classify new, unseen bug reports.
-   **Model Persistence:** Saves the trained model pipeline for future use.

## 🛠️ Technology Stack

-   **Python 3.10+**
-   **scikit-learn:** For the machine learning pipeline and models.
-   **Pandas:** For data manipulation and loading.
-   **NLTK:** For natural language processing tasks (e.g., stopword removal).
-   **Joblib:** For saving and loading the trained model.

## 📂 Project Structure

```
ml-bug-triage/
├── data/
│   └── bugs.csv
├── models/
│   └── bug_triage_model.joblib
├── main.py
├── predict.py
├── requirements.txt
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
git clone [https://github.com/your-username/ml-bug-triage.git](https://github.com/your-username/ml-bug-triage.git)
cd ml-bug-triage
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

**2. Make a Prediction:**

Run the `predict.py` script to classify a new, sample bug report using the saved model.

```bash
python predict.py
```
The output will show the predicted team for the sample bug.

```
--- New Bug Report ---
Title: User profile picture is not updating
Description: When a user tries to upload a new profile picture, the front-end shows success, but the image remains the old one. The API call seems to be failing silently without any error message on the screen.
------------------------
✅ Predicted Assignee Team: Backend Team
```

## 📈 Future Improvements

-   **Build an API:** Wrap the prediction logic in a Flask or FastAPI service.
-   **Experiment with Models:** Try more advanced models like SVM, Logistic Regression, or deep learning models (LSTM, BERT).
-   **Hyperparameter Tuning:** Use `GridSearchCV` to find the optimal parameters for the model.
-   **More Data:** Integrate with a real bug-tracking system API (like Jira or GitHub) to train on a larger, more realistic dataset.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
