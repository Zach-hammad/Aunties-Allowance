# scripts/generate_fake_data.py

import pandas as pd
import random

def generate_fake_weekly_data(num_samples=50):
    data = []

    for _ in range(num_samples):
        meal_prep = random.choice([0, 1])
        carpool = random.choice([0, 1])
        transit = random.choice([0, 1])

        baseline_spend = 220  # average user baseline weekly spend ($)
        grocery = random.randint(30, 80)
        gas = random.randint(10, 50)

        # Simulate savings if user does good tasks
        savings = 0
        if meal_prep:
            savings += 20
        if carpool:
            savings += 15
        if transit:
            savings += 10

        total_spent = baseline_spend - savings + random.randint(-10, 10)

        target_saved = 1 if savings > 0 else 0
        amount_saved = savings

        row = {
            "meal_prep_done": meal_prep,
            "carpool_done": carpool,
            "transit_done": transit,
            "total_spent": total_spent,
            "grocery_spent": grocery,
            "gas_spent": gas,
            "target_saved": target_saved,
            "amount_saved": amount_saved
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_fake_weekly_data()
    df.to_csv("data/weekly_behavior.csv", index=False)
    print("[SUCCESS] Fake weekly_behavior.csv created!")
