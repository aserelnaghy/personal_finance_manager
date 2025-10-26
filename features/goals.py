import os
from persistence.load_save_json import load_json, save_json

def check_goals_progress(user_id, transactions, goals):
    """
    Improved version: includes validation, goal status, and remaining amount.
    """
    if user_id not in goals or not transactions:
        return []

    net_savings = sum(
        t["amount"] if t["type"] == "income" else -t["amount"]
        for t in transactions if t["user_id"] == user_id
    )

    progress = []
    for goal_name, target in goals[user_id].items():
        percent = min(100, round((net_savings / target) * 100, 2))
        status = "Completed" if percent >= 100 else "In Progress"
        remaining = max(0, target - net_savings)

        progress.append({
            "goal_name": goal_name,
            "progress_percent": percent,
            "target_amount": target,
            "current_savings": net_savings,
            "remaining": remaining,
            "status": status
        })

    return progress


def set_goal(user_id, goal_name, target_amount):
    """
    Add or update a financial goal for a user with folder validation
    and error handling.
    """
    try:
        # --- 1. Validate inputs ---
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id.")
        if not isinstance(goal_name, str) or not goal_name.strip():
            raise ValueError("Invalid goal name.")
        if not isinstance(target_amount, (int, float)) or target_amount <= 0:
            raise ValueError("Goal amount must be a positive number.")

        # --- 2. Ensure data directory exists ---
        os.makedirs("data", exist_ok=True)

        # --- 3. Load existing goals safely ---
        goals = {}
        try:
            goals = load_json("data/goals.json")
        except (FileNotFoundError, ValueError):
            print("Goals.json missing or invalid — creating a new one.")
            goals = {}

        # --- 4. Update goal ---
        goals.setdefault(user_id, {})
        goals[user_id][goal_name] = round(float(target_amount), 2)

        # --- 5. Save updated goals ---
        save_json(goals, "data/goals.json")
        print(f"Goal '{goal_name}' set with target {target_amount} for user {user_id}.")

    except ValueError as e:
        print(f"Input error: {e}")
    except PermissionError:
        print("Permission denied while accessing data directory.")
    except Exception as e:
        print(f"Unexpected error: {e}")
