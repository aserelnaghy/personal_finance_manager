from datetime import datetime, timedelta
from uuid import uuid4
from persistence.load_save_json import load_json, save_json
import os

def process_recurring_transactions(user_id, transactions):
    """
    Process due recurring transactions for a user.
    If 'recurring.json' doesn't exist, create it automatically.

    Args:
        user_id (str): ID of the user to process.
        transactions (list): Existing list of transactions.

    Returns:
        list: Updated list of transactions including new recurring ones.
    """
    try:
        # --- 1. Ensure data directory exists ---
        os.makedirs("data", exist_ok=True)

        recurring_path = "data/recurring.json"

        # --- 2. If recurring.json doesn't exist, create it empty ---
        if not os.path.exists(recurring_path):
            print("Recurring.json not found — creating a new one.")
            save_json({}, recurring_path)  # start with empty dict

        # --- 3. Load recurring data safely ---
        recurring_data = load_json(recurring_path)
        if not isinstance(recurring_data, dict):
            print("Recurring.json corrupted — resetting file.")
            recurring_data = {}
            save_json(recurring_data, recurring_path)

        # --- 4. Get user’s recurring list ---
        recurring_list = recurring_data.get(user_id, [])
        if not recurring_list:
            print(f"No recurring transactions found for user {user_id}.")
            return transactions

        # --- 5. Process due recurring transactions ---
        today = datetime.now().strftime("%Y-%m-%d")
        new_transactions = []

        for r in recurring_list:
            if r["next_date"] <= today:
                # Schedule next trigger
                next_date = (
                    datetime.strptime(today, "%Y-%m-%d")
                    + timedelta(days=r["interval_days"])
                ).strftime("%Y-%m-%d")
                r["next_date"] = next_date

                # Create new transaction
                txn = {
                    "transaction_id": f"RC-{uuid4().hex[:6]}",
                    "user_id": user_id,
                    "type": r["type"],
                    "amount": r["amount"],
                    "category": r["category"],
                    "date": today,
                    "description": f"Recurring: {r['description']}",
                    "payment_method": r["payment_method"],
                }
                new_transactions.append(txn)

        # --- 6. Update recurring.json with new next_date values ---
        recurring_data[user_id] = recurring_list
        save_json(recurring_data, recurring_path)

        # --- 7. Append new transactions ---
        if new_transactions:
            transactions.extend(new_transactions)
            print(f"{len(new_transactions)} recurring transactions processed for {user_id}.")
        else:
            print(f"No due recurring transactions for {user_id} today.")

        return transactions

    except PermissionError:
        print("Permission denied while accessing recurring.json.")
        return transactions
    except Exception as e:
        print(f"Unexpected error while processing recurring transactions: {e}")
        return transactions