import os
import datetime
from utils.ids import generate_transaction_id
from utils.date_utils import get_today_str
from persistence.load_save_json import load_json, save_json
from auth.user_manager import get_current_user
from utils.errors import InvalidTransactionError, UserNotFoundError
from config import TRANSACTION_FILE


def add_transaction(transaction_type, amount, category, description, payment_method):
    """ Add an income or expense transaction for the current user."""
    user = get_current_user()

    if not user:
        raise UserNotFoundError("No active user found. Please log in first.")

    transaction = load_json(TRANSACTION_FILE)

    new_transaction = {
        "transation_id": generate_transaction_id(),
        "user_id": user["user_id"],
        "type": transaction_type.lower(),
        "amount": float(amount),
        "category": category,
        "date": get_today_str(),
        "description": description,
        "payment_method": payment_method
    }

    transaction.append(new_transaction)
    save_json(transaction, TRANSACTION_FILE)

    print(f"Transaction added successfully: {new_transaction['transaction_id']}")
    return new_transaction


def view_transacation (user_only=True):
    """View transactions (default for the current user only)"""
    
    user = get_current_user()
    transactions = load_json(TRANSACTION_FILE)

    if user_only:
        user_txns = [t for t in transactions if t["user_id"] == user["user_id"]]
    else:
        user_txns = transactions

    if not user_txns:
        print("No Transactions found.")
        return []
    
    for txn in user_txns:
        print(f"[ {txn['transaction_id']} | {txn['date']} | {txn['type'].capitalize()} | {txn['category']} | {txn['amount']} ]")
    return user_txns



def edit_transaction(transaction_id, **updates):
    """Edit a transaction by ID (for the current user)."""
    user = get_current_user()
    transactions = load_json(TRANSACTION_FILE)
    updated = False

    for txn in transactions:
        if txn["transaction_id"] == transaction_id and txn["user_id"] == user["user_id"]:
            txn.update({k: v for k, v in updates.items() if v is not None})
            updated = True
            break

    if not updated:
        raise InvalidTransactionError("Transaction not found or access denied.")

    save_json(TRANSACTION_FILE, transactions)
    print(f"Transaction {transaction_id} updated successfully.")


def delete_transaction(transaction_id, confirm=True):
    """Delete a transaction by ID, with optional confirmation."""
    user = get_current_user()
    transactions = load_json(TRANSACTION_FILE)
    remaining = [t for t in transactions if not (t["transaction_id"] == transaction_id and t["user_id"] == user["user_id"])]

    if len(remaining) == len(transactions):
        raise InvalidTransactionError("Transaction not found or access denied.")

    if confirm:
        choice = input(f"Are you sure you want to delete transaction {transaction_id}? (y/n): ")
        if choice.lower() != "y":
            print("Deletion cancelled.")
            return

    save_json(TRANSACTION_FILE, remaining)
    print(f"Transaction {transaction_id} deleted successfully.")
