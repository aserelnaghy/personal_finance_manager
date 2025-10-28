from utils.ids import generate_transaction_id
from utils.date_utils import get_today_str, parse_date
from persistence.load_save_json import load_json, save_json
from auth.user_manager import get_current_user
from utils.errors import InvalidTransactionError, UserNotFoundError
from config import *


def add_transaction(type, amount, category, description, payment_method):
    """ Add an income or expense transaction for the current user."""
    user = get_current_user()

    if not user:
        raise UserNotFoundError("No active user found. Please log in first.")

    transaction = load_json(TRANSACTIONS_FILE)

    new_transaction = {
        "transaction_id": generate_transaction_id(),
        "user_id": user["user_id"],
        "type": type.lower(),
        "amount": float(amount),
        "category": category,
        "date": get_today_str(),
        "description": description,
        "payment_method": payment_method
    }

    transaction.append(new_transaction)
    save_json(transaction, TRANSACTIONS_FILE)

    print(f"Transaction added successfully: {new_transaction['transaction_id']}")
    return new_transaction


def view_transaction(user_only=True):
    """View transactions (default for the current user only)"""
    
    user = get_current_user()
        # Handle case where not logged in
    if not user:
        raise UserNotFoundError("No active user found. Please log in first.")

    transactions = load_json(TRANSACTIONS_FILE)

    # Handle case where transactions file doesn't exist or is empty
    if not transactions:
        print("No transactions found in the system.")
        return []
    transactions = load_json(TRANSACTIONS_FILE)

    if user_only:
        user_txns = [t for t in transactions if t["user_id"] == user["user_id"]]
    else:
        user_txns = transactions

    if not user_txns:
        print("No Transactions found.")
        return []
    

    return user_txns



def edit_transaction(transaction_id, **updates):
    """Edit a transaction by ID (for the current user)."""
    user = get_current_user()
    transactions = load_json(TRANSACTIONS_FILE)
    updated = False

    for txn in transactions:
        if txn["transaction_id"] == transaction_id and txn["user_id"] == user["user_id"]:
            txn.update({k: v for k, v in updates.items() if v is not None})
            updated = True
            break

    if not updated:
        raise InvalidTransactionError("Transaction not found or access denied.")

    save_json(transactions, TRANSACTIONS_FILE)
    print(f"Transaction {transaction_id} updated successfully.")


def delete_transaction(transaction_id, confirm=True):
    """Delete a transaction by ID, with optional confirmation."""
    user = get_current_user()
    transactions = load_json(TRANSACTIONS_FILE)
    remaining = [t for t in transactions if not (t["transaction_id"] == transaction_id and t["user_id"] == user["user_id"])]

    if len(remaining) == len(transactions):
        raise InvalidTransactionError("Transaction not found or access denied.")

    if confirm:
        choice = input(f"Are you sure you want to delete transaction {transaction_id}? (y/n): ")
        if choice.lower() != "y":
            print("Deletion cancelled.")
            return

    save_json(remaining, TRANSACTIONS_FILE)
    print(f"Transaction {transaction_id} deleted successfully.")



def search_transactions(user_id, start_date=None, end_date=None,
                        category=None, type=None, min_amount=None, max_amount=None,
                        sort_by=None, descending=False):
    """
    Search and filter transactions for a specific user.

    Parameters:
        user_id (str): The user whose transactions to filter.
        start_date (str): ISO date string 'YYYY-MM-DD' for start of range.
        end_date (str): ISO date string 'YYYY-MM-DD' for end of range.
        category (str): Category to filter by.
        min_amount (float): Minimum transaction amount.
        max_amount (float): Maximum transaction amount.
        sort_by (str): One of ['date', 'amount', 'category', 'type'].
        descending (bool): Sort order.

    Returns:
        List of filtered transactions.
    """

    # --- Validation layer ---
    if not isinstance(user_id, str) or not user_id.strip():
        raise InvalidTransactionError("Invalid user_id provided.")

    # Validate and parse dates if provided
    start = end = None
    if start_date:
        try:
            start = parse_date(start_date)
        except ValueError:
            raise InvalidTransactionError("start_date must be in 'YYYY-MM-DD' format.")

    if end_date:
        try:
            end = parse_date(end_date)
        except ValueError:
            raise InvalidTransactionError("end_date must be in 'YYYY-MM-DD' format.")

    # Ensure chronological order
    if start and end and end < start:
        raise InvalidTransactionError("end_date cannot be earlier than start_date.")

    # Validate numeric filters
    if min_amount is not None:
        try:
            min_amount = float(min_amount)
        except ValueError:
            raise InvalidTransactionError("min_amount must be a number.")

    if max_amount is not None:
        try:
            max_amount = float(max_amount)
        except ValueError:
            raise InvalidTransactionError("max_amount must be a number.")

    if type and type.lower() not in ['income', 'expense']:
        raise InvalidTransactionError("type must be 'income' or 'expense'.")

    # Validate sorting field
    valid_sort_keys = ("date", "amount", "category")
    if sort_by and sort_by not in valid_sort_keys:
        raise InvalidTransactionError(f"sort_by must be one of {valid_sort_keys}.")

    # --- Load data ---
    all_transactions = load_json(TRANSACTIONS_FILE)
    if not isinstance(all_transactions, list):
        raise InvalidTransactionError("Invalid transactions data format (expected list).")

    results = [txn for txn in all_transactions if txn.get("user_id") == user_id]

    # --- Apply filters ---
    if start:
        results = [t for t in results if parse_date(t["date"]) >= start]

    if end:
        results = [t for t in results if parse_date(t["date"]) <= end]

    if category:
        results = [t for t in results if t.get("category", "").lower() == category.lower()]

    if type:
        results = [t for t in results if t.get("type", "").lower() == type.lower()]

    if min_amount is not None:
        results = [t for t in results if float(t.get("amount", 0)) >= min_amount]

    if max_amount is not None:
        results = [t for t in results if float(t.get("amount", 0)) <= max_amount]

    # --- Sorting (added transaction 'type' support) ---
    if sort_by:
        results.sort(
            key=lambda x: x.get(sort_by, "").lower() if isinstance(x.get(sort_by), str)
            else x.get(sort_by, 0),
            reverse=descending
        )

    return results

