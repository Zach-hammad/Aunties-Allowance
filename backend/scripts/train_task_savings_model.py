import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_model():
    df = pd.read_csv("data/synthetic_task_savings_data.csv")

    features = ["meal_prep_done", "carpool_done", "transit_done", "grocery_spent", "gas_spent", "total_spent"]
    target = "target_savings"

    X = df[features]
    y = df[target]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model
    joblib.dump(model, "ml_models/task_savings_model.joblib")
    print("[SUCCESS] Task savings model trained and saved at ml_models/task_savings_model.joblib")

if __name__ == "__main__":
    train_model()
