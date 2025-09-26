import joblib
from main import preprocess_text # Reuse the same preprocessing function

def predict_team(bug_title, bug_description):
    """
    Loads the trained model and predicts the assignee team for a new bug.
    """
    # Load the saved model pipeline
    try:
        model = joblib.load('models/bug_triage_model.joblib')
    except FileNotFoundError:
        return "Model not found. Please run main.py to train and save the model first."

    # Combine and preprocess the new bug report
    bug_text = bug_title + ' ' + bug_description
    clean_bug_text = preprocess_text(bug_text)

    # The model pipeline expects a list or iterable of texts
    prediction = model.predict([clean_bug_text])

    # The prediction is an array, so we get the first element
    return prediction[0]

if __name__ == "__main__":
    # --- Example of a new bug report ---
    new_bug_title = "User profile picture is not updating"
    new_bug_description = "When a user tries to upload a new profile picture, the front-end shows success, but the image remains the old one. The API call seems to be failing silently without any error message on the screen."

    # Get the prediction
    predicted_team = predict_team(new_bug_title, new_bug_description)

    print("--- New Bug Report ---")
    print(f"Title: {new_bug_title}")
    print(f"Description: {new_bug_description}")
    print("------------------------")
    print(f"✅ Predicted Assignee Team: {predicted_team}")

    print("\n--- Another Example ---")
    another_bug_title = "Page crashes on mobile Safari"
    another_bug_description = "The home page completely freezes and then crashes when viewed on an iPhone using Safari. It works fine on Chrome. Looks like a rendering or JavaScript compatibility issue."
    predicted_team_2 = predict_team(another_bug_title, another_bug_description)
    print(f"✅ Predicted Assignee Team: {predicted_team_2}")
    