from typing import Optional
from auth.user_manager import get_current_user, login_user, create_user, logout_user
from transactions.transaction_manager import add_transaction, view_transaction, edit_transaction, delete_transaction, search_transactions
from reports.reports_manager import (
    generate_dashboard_summary, generate_monthly_report,
    generate_category_breakdown, generate_spending_trends)
from persistence.load_save_json import load_json
from config import TRANSACTIONS_FILE
# from features.budgets import set_budget, get_budget, check_budget_alerts
# from features.goals import set_savings_goal, get_goal_progress, update_goal_progress
# from features.financial_health import calculate_financial_health_score
from ui.input_validators import *
from utils.date_utils import get_today_str, parse_date

def prompt_register() -> bool:
    """Prompt user for registration details."""
    print("\n=== User Registration ===")
    
    username = input("Enter username: ").strip()
    pin = input("Enter a 4-digit PIN: ").strip()
    
    try:
        user = create_user(username, pin)
        print(f"User '{user['name']}' registered successfully!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def prompt_login() -> bool:
    """Prompt user for login credentials."""
    print("\n=== Login ===")
    
    username = input("Username: ").strip()
    pin = input("PIN: ").strip()
    
    try:
        user = login_user(username, pin)
        print(f"Welcome, {user['name']}!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def prompt_logout() -> None:
    """Logs out the current user."""
    logout_user()
    print("You have been logged out.")


def prompt_add_transaction() -> Optional[dict]:
    """Prompt user to add a transaction."""
    print("\n=== Add Transaction ===")
    
    try:
        type = input("Type (income/expense): ").strip().lower()
        if type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'.")
    except ValueError as e:
        print(f"Error: {e}")
        return None

    amount = input("Amount: ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            print("Amount must be greater than zero.")
            return None
    except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return None

    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return None
            
    description = input("Description: ").strip()
    if not description:
        description = "No description provided."

    payment_method = input("Payment Method: ").strip()
    if not payment_method:
        print("Payment method cannot be empty.")
        return None

    transaction = add_transaction(type, float(amount), category, description, payment_method)
    print(f"Transaction added : {transaction}")
    return transaction


def prompt_view_transaction() -> None:
    """ prompt user to view only the logged in user's transactions."""
    print("\n=== View Transactions ===")
    try:
        transactions = view_transaction(user_only=True)
        if not transactions:
            print("No transactions to display.")

        print("\n" + "=" * 65)
        print(f"{'ID':<10} | {'Date':<12} | {'Type':<8} | {'Category':<12} | {'Amount':>10}")
        print("-" * 65)

        # Print each transaction in table format
        for txn in transactions:
            txn_id = txn.get('transaction_id', 'N/A')[:10]
            date = txn.get('date', 'N/A')
            txn_type = txn.get('type', 'N/A').capitalize()
            category = txn.get('category', 'N/A')
            amount = txn.get('amount', 0.0)
            print(f"{txn_id:<10} | {date:<12} | {txn_type:<8} | {category:<12} | ${amount:>9.2f}")

        print("=" * 65)
        print(f"Total transactions: {len(transactions)}\n")
        return transactions
    
    except Exception as e:
        print(f"Unexpected Error: {e}")

def prompt_edit_transactions() -> Optional[dict]:
    """Prompt the user to edit an existing transaction via the CLI."""
    print("\n=== Edit Transaction ===")

    try:
        # Ask for transaction ID
        transaction_id = input("Enter the Transaction ID to edit: ").strip()
        if not transaction_id:
            print("Transaction ID cannot be empty.")
            return None

        print("Leave a field blank if you do NOT want to change it.\n")

        # Prompt for possible updates
        new_type = input("New Type (income/expense): ").strip().lower()
        if new_type and new_type not in ("income", "expense"):
            print("Invalid type. Please enter 'income' or 'expense'.")
            return None

        new_amount_str = input("New Amount: ").strip()
        new_amount = None
        if new_amount_str:
            try:
                new_amount = float(new_amount_str)
                if new_amount <= 0:
                    print("Amount must be greater than zero.")
                    return None
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
                return None

        new_category = input("New Category: ").strip() or None
        new_description = input("New Description: ").strip() or None
        new_payment_method = input("New Payment Method: ").strip() or None

        # Call backend function
        edit_transaction(
            transaction_id,
            type=new_type or None,
            amount=new_amount,
            category=new_category,
            description=new_description,
            payment_method=new_payment_method
        )

        print(f"Transaction {transaction_id} updated successfully.")
        return {
            "transaction_id": transaction_id,
            "type": new_type,
            "amount": new_amount,
            "category": new_category,
            "description": new_description,
            "payment_method": new_payment_method
        }
    
    except Exception as e:
        print(f"Error updating transaction: {e}")
        return None

def prompt_delete_transactions() -> Optional[str]:
    """Prompt the user to delete a transaction through the CLI."""
    print("\n=== Delete Transaction ===")

    try:
        # Ask for transaction ID
        transaction_id = input("Enter the Transaction ID to delete: ").strip()
        if not transaction_id:
            print("Transaction ID cannot be empty.")
            return None

        # Ask for confirmation
        confirm_choice = input(f"Are you sure you want to delete transaction {transaction_id}? (y/n): ").strip().lower()
        if confirm_choice not in ("y", "n"):
            print("Invalid choice. Please enter 'y' or 'n'.")
            return None
        if confirm_choice == "n":
            print("Deletion cancelled by user.")
            return None

        # Call backend logic (no second confirmation needed)
        delete_transaction(transaction_id, confirm=False)

        print(f"Transaction {transaction_id} deleted successfully.")
        return transaction_id
    
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return None

def prompt_search_transactions():
    """CLI interface for searching and filtering transactions with user-friendly prompts."""
    print("\nTransaction Search Filters")
    print("-" * 35)
    print("You can filter your transactions by one or more of the following:")
    print("1. Date Range (Start and End)")
    print("2. Category")
    print("3. Type (income or expense)")
    print("4. Amount Range (Min and Max)")
    print("5. Sort Results")
    print("6. No Filter (show all transactions)\n")

    try:
        user = get_current_user()
        if not user:
            print("You must be logged in to search transactions.")
            return

        user_id = user["user_id"]

        # Initialize all filters to None
        start_date = end_date = category = txn_type = sort_by = None
        min_amount = max_amount = None
        descending = False

        # Ask which filters to apply
        filters_chosen = input(
            "Enter the numbers of the filters you want to apply (comma-separated, e.g. 1,3,5): "
        ).strip()

        valid_choices = {"1", "2", "3", "4", "5", "6"}
        selected_filters = {f.strip() for f in filters_chosen.split(",") if f.strip()}

        # Validate input
        if not selected_filters.issubset(valid_choices):
            print("Invalid selection. Please enter numbers between 1 and 6.")
            return

        if "1" in selected_filters:  # Date range
            start_date = input("Start date (YYYY-MM-DD) or leave blank: ").strip() or None
            end_date = input("End date (YYYY-MM-DD) or leave blank: ").strip() or None

            # Quick validation before backend
            for label, date_str in [("Start", start_date), ("End", end_date)]:
                if date_str:
                    try:
                        parse_date(date_str)
                    except ValueError:
                        print(f"{label} date must be in YYYY-MM-DD format.")
                        return

        if "2" in selected_filters:  # Category
            category = input("Enter category to filter by: ").strip() or None

        if "3" in selected_filters:  # Type
            txn_type = input("Enter transaction type (income/expense): ").strip().lower()
            if txn_type not in ("income", "expense"):
                print("Invalid type. Must be 'income' or 'expense'.")
                return

        if "4" in selected_filters:  # Amount range
            try:
                min_amount_input = input("Minimum amount (or leave blank): ").strip()
                max_amount_input = input("Maximum amount (or leave blank): ").strip()
                min_amount = float(min_amount_input) if min_amount_input else None
                max_amount = float(max_amount_input) if max_amount_input else None
            except ValueError:
                print("Amounts must be numeric.")
                return

        if "5" in selected_filters:  # Sorting
            print("\nSort options: date | amount | category")
            sort_by = input("Sort by: ").strip().lower()
            if sort_by not in ("date", "amount", "category", ""):
                print("Invalid sort field.")
                return
            order = input("Descending order? (y/n): ").strip().lower()
            descending = order == "y"

        # --- Fetch results ---
        transactions = search_transactions(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            category=category,
            type=txn_type,
            min_amount=min_amount,
            max_amount=max_amount,
            sort_by=sort_by,
            descending=descending
        )

        # --- Display results ---
        if not transactions:
            print("\nNo transactions found with the given filters.")
            return

        print("\nFiltered Transactions:")
        print("\n" + "=" * 65)
        print(f"{'ID':<10} | {'Date':<12} | {'Type':<8} | {'Category':<12} | {'Amount':>10}")
        print("-" * 65)

        for txn in transactions:
            print(
                f"{txn.get('transaction_id', ''):<10} "
                f"{txn.get('date', ''):<12} "
                f"{txn.get('type', ''):<8} "
                f"{txn.get('category', ''):<15} "
                f"{txn.get('amount', 0):<10.2f} "
                f"{txn.get('description', '')}"
            )
        print("-" * 65)
        print(f"Total transactions found: {len(transactions)}\n")
    
    except Exception as e:
        print(f"Error during search: {e}")

