import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# One-time download for stopwords
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

# --- 1. Text Preprocessing Function ---
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

# --- 2. Main Training Logic ---
if __name__ == "__main__":
    print("Starting the bug triage model training process...")

    # Load the dataset
    df = pd.read_csv('data/bugs.csv')
    print(f"Loaded {len(df)} bug reports.")

    # Combine title and description into a single feature
    df['text'] = df['title'] + ' ' + df['description']

    # Apply preprocessing
    print("Preprocessing text data...")
    df['clean_text'] = df['text'].apply(preprocess_text)

    # Define features (X) and target (y)
    X = df['clean_text']
    y = df['assignee_team']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

    # --- 3. Create a Model Pipeline ---
    # A pipeline bundles the vectorizer and the classifier together.
    # This makes it easy to apply the same transformations to new data.
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))), # Use unigrams and bigrams
        ('classifier', MultinomialNB())
    ])

    # --- 4. Train the Model ---
    print("Training the model...")
    model_pipeline.fit(X_train, y_train)
    print("Model training complete.")

    # --- 5. Evaluate the Model ---
    print("\n--- Model Evaluation ---")
    y_pred = model_pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    # --- 6. Save the Model ---
    model_filename = 'models/bug_triage_model.joblib'
    joblib.dump(model_pipeline, model_filename)
    print(f"Model saved successfully to {model_filename}")
    