#!/usr/bin/env python3
# backend/scripts/train_with_auto_labels.py

import os
import json
import numpy as np
import pandas as pd
import joblib
from datetime import timedelta
from sklearn.ensemble import RandomForestRegressor

from config import PLAID_CLIENT
from services.finance_utils import fetch_recent_transactions, calculate_food_spending

def build_weekly_features(transactions, days_back=180):
    """Bucket each txn into the Sunday-ending week it belongs to."""
    # Convert Plaid models → dicts
    recs = [(t.to_dict() if hasattr(t, "to_dict") else t) for t in transactions]
    df = pd.DataFrame(recs)
    df['date'] = pd.to_datetime(df['date'])
    # Sunday of each week (Mon=0…Sun=6)
    df['week_start'] = (
        df['date'] + pd.to_timedelta(6 - df['date'].dt.weekday, unit='d')
    ).dt.date

    rows = []
    for wk, grp in df.groupby('week_start'):
        txns = grp.to_dict('records')
        rows.append({
            'week_start':    wk,
            'grocery_spent': calculate_food_spending(txns),
            'gas_spent':     sum(t['amount'] for t in txns if 'gas' in t['name'].lower()),
            'total_spent':   grp['amount'].sum()
        })
    return pd.DataFrame(rows)

def generate_synthetic_labels(n, seed=42, noise_std=5):
    """Produce synthetic meal/carpool/transit flags + savings for n samples."""
    np.random.seed(seed)
    meals    = np.random.randint(0,2, size=n)
    carpools = np.random.randint(0,2, size=n)
    transits = np.random.randint(0,2, size=n)
    savings  = (
        meals*30 +
        carpools*20 +
        transits*25 +
        np.random.normal(0, noise_std, size=n)
    )
    savings = np.clip(savings, 0, None)
    return pd.DataFrame({
        'meal_prep_done':  meals,
        'carpool_done':    carpools,
        'transit_done':    transits,
        'target_savings':  np.round(savings,2)
    })

def main():
    # 1) Fetch an extended Plaid history
    token_path = os.path.join(os.path.dirname(__file__), 'access_token.json')
    with open(token_path) as f:
        access_token = json.load(f)['access_token']

    print("🔗 Fetching 180 days of Plaid transactions…")
    txns = fetch_recent_transactions(PLAID_CLIENT, access_token, days_back=180)

    # 2) Build weekly features
    print("⚙️  Aggregating weekly features…")
    df_feats = build_weekly_features(txns, days_back=180)
    print(f"→ Found {len(df_feats)} weekly feature rows")

    # 3) Auto-generate synthetic labels for each week
    df_labels = generate_synthetic_labels(len(df_feats), seed=123)
    df_full   = pd.concat([df_feats.reset_index(drop=True), df_labels], axis=1)

    # 4) Save the expanded final_habits CSV
    out_data = df_full[['week_start','meal_prep_done','carpool_done','transit_done','target_savings']]
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'final_habits_auto.csv')
    out_data.to_csv(csv_path, index=False)
    print(f"[✅] Auto-generated labels written to {csv_path}")

    # 5) Train on the full synthetic+real features
    X = df_full[['grocery_spent','gas_spent','total_spent','meal_prep_done','carpool_done','transit_done']]
    y = df_full['target_savings']

    print("📈 Training RandomForest on expanded dataset…")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 6) Save the model
    model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ml_models'))
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'plaid_savings_model_expanded.joblib')
    joblib.dump(model, model_path)
    print(f"[✅] Trained model saved to {model_path}")

if __name__ == "__main__":
    main()
