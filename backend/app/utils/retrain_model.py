import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
import os

def retrain_model():
    # Load data
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "Crop_recommendation.csv")
    df = pd.read_csv(dataset_path)
    
    # Data Preprocessing
    X = df.drop("label", axis=1)  # Features (assuming "label" is the target column)
    y = df["label"]  # Target variable
    
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [10, 20, None],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "bootstrap": [True, False]
    }
    
    grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    
    # Best model after hyperparameter tuning
    best_model = grid_search.best_estimator_
    
    # Save the retrained model
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "crop_model.pkl")
    joblib.dump(best_model, model_path)
    
    print("Model retrained and saved successfully!")

