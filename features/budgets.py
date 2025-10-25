# budgets.py
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
        print(f"✅ All budgets are within limits for user {user_id}.")

    return alerts



