import pandas as pd
import numpy as np

np.random.seed(42)  # for reproducibility

def generate_data(n_samples=1000):
    data = []
    for _ in range(n_samples):
        meal_prep = np.random.choice([0, 1])
        carpool = np.random.choice([0, 1])
        transit = np.random.choice([0, 1])

        grocery_spent = np.random.normal(50, 15)  # average $50 groceries
        gas_spent = np.random.normal(30, 10)      # average $30 gas
        total_spent = grocery_spent + gas_spent + np.random.normal(50, 20)  # total including other stuff

        # Now create a target_savings with realistic logic
        savings = 0
        if meal_prep:
            savings += 30  # save $30 by not eating out
        if carpool:
            savings += 20  # save $20 on gas
        if transit:
            savings += 25  # save $25 compared to driving

        # Add a little noise
        savings += np.random.normal(0, 5)

        savings = max(savings, 0)  # can't have negative savings

        data.append({
            "meal_prep_done": meal_prep,
            "carpool_done": carpool,
            "transit_done": transit,
            "grocery_spent": round(grocery_spent, 2),
            "gas_spent": round(gas_spent, 2),
            "total_spent": round(total_spent, 2),
            "target_savings": round(savings, 2)
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/synthetic_task_savings_data.csv", index=False)
    print("[SUCCESS] Synthetic training data created at data/synthetic_task_savings_data.csv")
