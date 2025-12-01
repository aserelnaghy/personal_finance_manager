from datetime import datetime, timedelta
from uuid import uuid4
from persistence.load_save_json import load_json, save_json
from auth.user_manager import get_current_user
from utils.ids import generate_transaction_id
from utils.date_utils import get_today_str
from config import TRANSACTIONS_FILE

def process_recurring_transactions():
    """Check and add new instances of due recurring transactions."""
    user = get_current_user()
    if not user:
        print("No active user. Please log in first.")
        return

    transactions = load_json(TRANSACTIONS_FILE)
    today = datetime.strptime(get_today_str(), "%Y-%m-%d")

    user_txns = [
        t for t in transactions
        if t["user_id"] == user["user_id"] and t.get("is_recurring")
    ]

    if not user_txns:
        return  # silently skip if no recurring transactions

    added_count = 0
    for txn in user_txns:
        try:
            last_date = datetime.strptime(txn["date"], "%Y-%m-%d")
            interval = txn.get("recurrence_interval")

            if interval == "daily":
                next_due = last_date + timedelta(days=1)
            elif interval == "weekly":
                next_due = last_date + timedelta(weeks=1)
            elif interval == "monthly":
                next_due = last_date + timedelta(days=30)
            else:
                continue

            if today >= next_due:
                new_txn = txn.copy()
                new_txn["transaction_id"] = generate_transaction_id()
                new_txn["date"] = get_today_str()
                transactions.append(new_txn)
                added_count += 1

        except Exception as e:
            print(f"Error processing transaction {txn.get('transaction_id')}: {e}")

    if added_count > 0:
        save_json(transactions, TRANSACTIONS_FILE)
        print(f"{added_count} recurring transaction(s) added automatically.")