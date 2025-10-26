# budgets.py
import os
from persistence.load_save_json import load_json, save_json

def check_budget_limits(user_id, transactions, budgets, verbose=True):
    """
    Check if a user exceeded any of their budget limits.

    Args:
        user_id (str): The user's ID.
        transactions (list): List of user's transactions (dicts).
        budgets (dict): Dict containing user budgets by category.
        verbose (bool): If True, print readable alerts.

    Returns:
        list: A list of alert dictionaries with category, spent, and limit.
    """

    alerts = []

    for category, limit in budgets.get(user_id, {}).items():
        spent = sum(
            t["amount"]
            for t in transactions
            if t["user_id"] == user_id
            and t["category"] == category
            and t["type"] == "expense"
        )
        if spent > limit:
            alert = {
                "category": category,
                "spent": spent,
                "limit": limit,
                "over_by": spent - limit,
            }
            alerts.append(alert)

            if verbose:
                print(
                    f"Budget exceeded for '{category}': "
                    f"spent {spent}, limit {limit} (over by {spent - limit})"
                )

    if not alerts and verbose:
        print(f"All budgets are within limits for user {user_id}.")

    return alerts


def set_budget_limit(user_id, category, limit):
    """
    Add or update a budget limit for a user with folder validation
    and error handling.
    """
    try:
        # --- 1. Validate inputs ---
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id.")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Invalid category name.")
        if not isinstance(limit, (int, float)) or limit <= 0:
            raise ValueError("Budget limit must be a positive number.")

        # --- 2. Ensure data directory exists ---
        os.makedirs("data", exist_ok=True)

        # --- 3. Load existing budgets safely ---
        budgets = {}
        try:
            budgets = load_json("data/budgets.json")
        except (FileNotFoundError, ValueError):
            print("budgets.json missing or invalid — creating a new one.")
            budgets = {}

        # --- 4. Update user’s budget data ---
        budgets.setdefault(user_id, {})
        budgets[user_id][category] = round(float(limit), 2)

        # --- 5. Save updated budgets ---
        save_json(budgets, "data/budgets.json")
        print(f"Budget for '{category}' set to {limit} for user {user_id}.")

    except ValueError as e:
        print(f"Input error: {e}")
    except PermissionError:
        print("Permission denied while accessing data directory.")
    except Exception as e:
        print(f"Unexpected error: {e}")