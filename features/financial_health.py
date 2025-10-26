from goals import check_goals_progress

def calculate_financial_health(user_id, transactions, goals):
    """
    Calculate a financial health score (0–100) for a user
    based on income/expense ratio and goal progress.

    Args:
        user_id (str): The user's ID
        transactions (list): List of user transactions
        goals (dict): User goals data

    Returns:
        float: Financial health score between 0 and 100
    """

    # --- 1- Calculate totals ---
    total_income = sum(
        t["amount"] for t in transactions
        if t["user_id"] == user_id and t["type"] == "income"
    )
    total_expense = sum(
        t["amount"] for t in transactions
        if t["user_id"] == user_id and t["type"] == "expense"
    )

    # --- 2- Compute savings ratio (0–1) ---
    savings_ratio = (
        (total_income - total_expense) / total_income
        if total_income > 0 else 0
    )

    # --- 3- Get average goal completion ---
    goals_progress = check_goals_progress(user_id, transactions, goals)
    avg_goal_completion = (
        sum(p for _, p in goals_progress) / len(goals_progress)
        if goals_progress else 0
    ) / 100  # convert to 0–1 scale

    # --- 4- Weighted score ---
    # 60% from savings, 40% from goal achievement
    score = (savings_ratio * 60) + (avg_goal_completion * 40)

    return round(score, 2)


if __name__ == "__main__":
    # Sample transactions
    transactions = [
        {"user_id": "user_1", "type": "income", "amount": 8000},
        {"user_id": "user_1", "type": "expense", "amount": 3000},
        {"user_id": "user_1", "type": "expense", "amount": 1000},
    ]

    # Sample goals
    goals = {
        "user_1": {"Buy Laptop": 10000, "Vacation": 4000}
    }

    # Test check_goals_progress
    print("=== Test Goals Progress ===")
    progress = check_goals_progress("user_1", transactions, goals)
    for goal, pct in progress:
        print(f"{goal}: {pct}%")

    # Test financial health score
    score = calculate_financial_health("user_1", transactions, goals)
    print(f"\nFinancial Health Score for user_1: {score}")
