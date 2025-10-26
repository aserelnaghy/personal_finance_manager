from datetime import datetime, timedelta
from uuid import uuid4

def process_recurring_transactions(user_id, recurring_list, transactions, today=None):
    """
    Process recurring transactions for a user.
    
    This function will:
    - Check if any recurring transaction is due today or earlier.
    - Add it to the transactions list.
    - Update its next_date for the next occurrence.
    
    Args:
        user_id (str): The ID of the user
        recurring_list (list): List of recurring transactions
        transactions (list): Current list of user transactions
        today (str, optional): Date to check against in 'YYYY-MM-DD'. Defaults to current date.
    
    Returns:
        list: Updated list of transactions
    """
    if today is None:
        today = datetime.now().strftime("%Y-%m-%d")

    for r in recurring_list:
        while r["next_date"] <= today:
            # Add the transaction
            transactions.append({
                "transaction_id": f"RC-{uuid4().hex[:6]}",  # unique ID
                "user_id": user_id,
                "type": r["type"],
                "amount": r["amount"],
                "category": r["category"],
                "date": r["next_date"],
                "description": f"Recurring: {r['description']}",
                "payment_method": r["payment_method"]
            })
            # Update next_date for the next occurrence
            next_dt = datetime.strptime(r["next_date"], "%Y-%m-%d") + timedelta(days=r["interval_days"])
            r["next_date"] = next_dt.strftime("%Y-%m-%d")

    return transactions





