import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# Define base directory

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MODEL_PATH = os.path.join(BASE_DIR, "backend", "app", "models", "crop_model.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "Crop_recommendation.csv")



def evaluate_model(model_path=MODEL_PATH, dataset_path=DATASET_PATH, threshold=0.85):
    """
    Evaluate the saved model using real test data.
    Returns True if accuracy >= threshold, else False.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found at {model_path}")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"❌ Dataset not found at {dataset_path}")

    # Load the model
    model = joblib.load(model_path)

    # Load dataset
    df = pd.read_csv(dataset_path)
    X = df.drop("label", axis=1)
    y = df["label"]

    # Split test data
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Predict and evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

    return accuracy >= threshold

if __name__ == "__main__":
    passed = evaluate_model()
    print("🎯 Evaluation Passed!" if passed else "⚠️ Evaluation Failed!")

