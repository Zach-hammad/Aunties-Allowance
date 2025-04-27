# scripts/train_task_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

def train_task_suggestion_model():
    # Load the data
    df = pd.read_csv("data/weekly_behavior.csv")

    # Define features and target
    feature_columns = ["meal_prep_done", "carpool_done", "transit_done", "grocery_spent", "gas_spent", "total_spent"]
    X = df[feature_columns]
    y = df["target_saved"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"[SUCCESS] Model trained with accuracy: {accuracy:.2f}")

    # Save model
    if not os.path.exists("ml_models"):
        os.makedirs("ml_models")
    joblib.dump(model, "ml_models/task_suggestion_model.joblib")
    print("[SUCCESS] Model saved to ml_models/task_suggestion_model.joblib")

if __name__ == "__main__":
    train_task_suggestion_model()
