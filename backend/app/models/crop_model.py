import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

# ✅ Dataset path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
dataset_path = os.path.join(BASE_DIR, "datasets", "Crop_recommendation.csv")
print(f"📁 Using dataset: {dataset_path}")

# ✅ Load dataset
df = pd.read_csv(dataset_path)
X = df.drop("label", axis=1)
y = df["label"]

# ✅ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Define model and hyperparameter grid
rf = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

# ✅ Apply GridSearchCV
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# ✅ Best model
best_model = grid_search.best_estimator_
print("🎯 Best Parameters:", grid_search.best_params_)
print(f"✅ Test Accuracy: {best_model.score(X_test, y_test):.2f}")

# ✅ Save model
model_path = os.path.join(BASE_DIR, "backend", "app", "models", "crop_model.pkl")
joblib.dump(best_model, model_path)
print(f"✅ Best model saved to {model_path}")
