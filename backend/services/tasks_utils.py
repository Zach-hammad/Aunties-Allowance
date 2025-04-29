import joblib
import pandas as pd
import itertools
from services.calendar_utils import find_free_time_slots
from services.scheduler_utils import schedule_tasks_into_free_slots

# Load model once
regressor_model = joblib.load("ml_models/plaid_savings_model_expanded.joblib")

# List of tasks
TASK_FEATURES = {
    "meal_prep": "meal_prep_done",
    "carpool": "carpool_done",
    "transit": "transit_done"
}

def generate_task_schedule(busy_slots, user_behavior, timezone):
    all_tasks = list(TASK_FEATURES.keys())
    best_savings = -1
    best_task_combo = []
    
    # Test all task combinations
    for r in range(1, len(all_tasks) + 1):
        for task_combo in itertools.combinations(all_tasks, r):
            simulated_behavior = user_behavior.copy()
            
            # Simulate doing only the tasks in task_combo
            for task in all_tasks:
                simulated_behavior[TASK_FEATURES[task]] = 1 if task in task_combo else 0
            
            # Create DataFrame with explicit column order matching the training data
            # Get feature names from the model
            feature_names = regressor_model.feature_names_in_  # scikit-learn 1.0+ stores feature names
            
            # Create DataFrame with exactly the same columns in the same order
            simulated_data = {}
            for feature in feature_names:
                simulated_data[feature] = [simulated_behavior.get(feature, 0)]
                
            simulated_df = pd.DataFrame(simulated_data)
            
            # Now prediction should work properly
            predicted_savings = regressor_model.predict(simulated_df)[0]
            
            if predicted_savings > best_savings:
                best_savings = predicted_savings
                best_task_combo = list(task_combo)
    
    suggested_tasks = best_task_combo
    
    # Then schedule best tasks
    free_slots = find_free_time_slots(busy_slots, timezone)
    scheduled_tasks = schedule_tasks_into_free_slots(suggested_tasks, free_slots, timezone)
    
    return scheduled_tasks
