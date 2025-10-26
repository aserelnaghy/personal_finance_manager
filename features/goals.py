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

