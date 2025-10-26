from typing import Optional
from auth.user_manager import get_current_user, login_user, create_user, logout_user
from transactions.transaction_manager import add_transaction, view_transaction, edit_transaction, delete_transaction, search_transactions
from reports.reports_manager import (
    generate_dashboard_summary, generate_monthly_report,
    generate_category_breakdown, generate_spending_trends)
from persistence.load_save_json import load_json, save_json
from config import TRANSACTIONS_FILE
from features.budgets import set_budget_limit, check_budget_limits
from features.goals import set_goal, check_goals_progress
from features.financial_health import calculate_financial_health
from features.recurring_processor import process_recurring_transactions
from ui.input_validators import *
from utils.date_utils import get_today_str, parse_date
from config import TRANSACTIONS_FILE, BUDGET_FILE, GOALS_FILE, RECURRING_FILE
from getpass import getpass

def prompt_register() -> bool:
    """Prompt user for registration details."""
    print("\n=== User Registration ===")
    
    username = input("Enter username: ").strip()
    pin = getpass("Enter PIN: ").strip()
    confirm_pin = getpass("Confirm PIN: ").strip()

    if pin != confirm_pin:
        print("Error: PINs do not match.")
        return False
    
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
    pin = getpass("PIN: ").strip()
    
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
        user = get_current_user()
        transactions = load_json(TRANSACTIONS_FILE)

        # Filter transactions for the current user
        user_transactions = [t for t in transactions if t.get("user_id") == user["user_id"]]

        # --- Validation: Check if there are any transactions to edit ---
        if not user_transactions:
            print("No transactions found. You must add one before editing.")
            return None

        # Optional: show existing transactions for context
        print("\nYour existing transactions:")
        for txn in user_transactions:
            print(f"  ID: {txn['transaction_id']} | {txn['type']} | {txn['category']} | {txn['amount']}")

        # --- Proceed with editing ---
        transaction_id = input("\nEnter the Transaction ID to edit: ").strip()
        if not transaction_id:
            print("Transaction ID cannot be empty.")
            return None

        # Validate that the transaction exists for this user
        if not any(txn["transaction_id"] == transaction_id for txn in user_transactions):
            print("Transaction ID not found or does not belong to you.")
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
        user = get_current_user()
        transactions = load_json(TRANSACTIONS_FILE)

        # Filter transactions for the current user
        user_transactions = [t for t in transactions if t.get("user_id") == user["user_id"]]

        # --- Validation: Check if there are any transactions to delete ---
        if not user_transactions:
            print("No transactions found. You must add one before attempting deletion.")
            return None

        # Optional: show user’s transactions for context
        print("\nYour existing transactions:")
        for txn in user_transactions:
            print(f"  ID: {txn['transaction_id']} | {txn['type']} | {txn['category']} | {txn['amount']}")

        # --- Ask for transaction ID ---
        transaction_id = input("\nEnter the Transaction ID to delete: ").strip()
        if not transaction_id:
            print("Transaction ID cannot be empty.")
            return None

        # Validate that the transaction exists for this user
        if not any(txn["transaction_id"] == transaction_id for txn in user_transactions):
            print("Transaction ID not found or does not belong to you.")
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

    try:
        user = get_current_user()
        if not user:
            print("You must be logged in to search transactions.")
            return

        user_id = user["user_id"]
        transactions = load_json(TRANSACTIONS_FILE)

        # Filter transactions for the current user
        user_transactions = [t for t in transactions if t.get("user_id") == user_id]

        # --- Validation: No transactions at all ---
        if not user_transactions:
            print("No transactions found. You must add one before using the search filters.")
            return


        print("\nTransaction Search Filters")
        print("-" * 35)
        print("You can filter your transactions by one or more of the following:")
        print("1. Date Range (Start and End)")
        print("2. Category")
        print("3. Type (income or expense)")
        print("4. Amount Range (Min and Max)")
        print("5. Sort Results")
        print("6. No Filter (show all transactions)\n")

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

def prompt_dashboard_summary():
    """Display the monthly dashboard summary in ASCII format (no colors)."""
    user = get_current_user()
    all_transactions = load_json(TRANSACTIONS_FILE)
    user_transactions = [t for t in all_transactions if t["user_id"] == user["user_id"]]

    if not user_transactions:
        print("\nNo transactions found for this user.\n")
        return

    summary = generate_dashboard_summary(user_transactions)
    name = user["name"]
    period = summary["period"]

    print("\n" + "=" * 60)
    print("            PERSONAL FINANCE MANAGER v1.0")
    print("=" * 60)
    print(f"User: {name}")
    print(f"Period: {period}")
    print("-" * 60)
    print(f"{'Total Income:':<25} ${summary['total_income']:,.2f}")
    print(f"{'Total Expenses:':<25} ${summary['total_expenses']:,.2f}")
    print(f"{'Net Savings:':<25} ${summary['net_savings']:,.2f}")
    print("-" * 60)
    print(f"{'Current Balance:':<25} ${summary['current_balance']:,.2f}")
    print("=" * 60)
    print("\nTop Spending Categories:")

    if summary["top_categories"]:
        for i, cat in enumerate(summary["top_categories"], start=1):
            print(f"{i}. {cat['category']:<15} ${cat['amount']:>8,.2f}   ({cat['percent']:>5.1f}%)")
    else:
        print("No expense transactions for this month.")
    print()


def prompt_monthly_report():
    """Prompt user for month and year to generate monthly report."""
    print("\n=== Monthly Report ===")
    print("-" * 40)

    try:
        user = get_current_user()
        if not user:
            print("You must be logged in to view reports.")
            return

        user_id = user["user_id"]

        # Load all transactions and filter by current user
        all_transactions = load_json(TRANSACTIONS_FILE)
        user_transactions = [t for t in all_transactions if t.get("user_id") == user_id]

        if not user_transactions:
            print("No transactions available to generate a report.")
            return

        # Generate the monthly report
        monthly_summary = generate_monthly_report(user_transactions)

        # Display formatted report
        print(f"\n{'Month':<10} {'Income':>12} {'Expense':>12} {'Balance':>12}")
        print("-" * 50)

        total_income = total_expense = 0

        for month, data in sorted(monthly_summary.items()):
            income = data.get("income", 0)
            expense = data.get("expense", 0)
            balance = income - expense
            total_income += income
            total_expense += expense

            print(f"{month:<10} {income:>12.2f} {expense:>12.2f} {balance:>12.2f}")

        print("-" * 50)
        print(f"{'TOTAL':<10} {total_income:>12.2f} {total_expense:>12.2f} {(total_income - total_expense):>12.2f}")
        print("-" * 50)

    except Exception as e:
        print(f"Unexpected error: {e}")

def prompt_category_breakdown():
    """Display spending or income breakdown by category."""
    print("\nCategory Breakdown")
    print("-" * 40)

    try:
        user = get_current_user()
        if not user:
            print("You must be logged in to view reports.")
            return

        user_id = user["user_id"]
        all_transactions = load_json(TRANSACTIONS_FILE)
        user_transactions = [t for t in all_transactions if t.get("user_id") == user_id]

        if not user_transactions:
            print("No transactions available to generate report.")
            return

        breakdown = generate_category_breakdown(user_transactions)

        if not breakdown:
            print(f"No expenses transactions found to analyze.")
            return

        print(f"\nExpenses Breakdown by Category:")
        print(f"{'Category':<20} {'Amount (EGP)':>15}")
        print("-" * 40)

        total = 0
        for category, amount in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:<20} {amount:>15.2f}")
            total += amount

        print("-" * 40)
        print(f"{'TOTAL':<20} {total:>15.2f}")
        print("-" * 40)

    except Exception as e:
        print(f"Unexpected error: {e}")

def prompt_spending_trends():
    """Display month-to-month spending changes for the current user."""
    print("\nSpending Trends Report")
    print("-" * 55)

    try:
        user = get_current_user()
        if not user:
            print("You must be logged in to view spending trends.")
            return

        user_id = user["user_id"]
        all_transactions = load_json(TRANSACTIONS_FILE)
        user_transactions = [t for t in all_transactions if t.get("user_id") == user_id]

        if not user_transactions:
            print("No transactions available to analyze trends.")
            return

        # Generate the monthly spending trends
        trends = generate_spending_trends(user_transactions)

        if not trends:
            print("Not enough monthly data to determine trends.")
            return

        print(f"{'From → To':<20} {'Change (EGP)':>15} {'% Change':>12} {'Trend':>8}")
        print("-" * 55)

        for t in trends:
            arrow = "⬆️" if t["change"] > 0 else ("⬇️" if t["change"] < 0 else "➡️")
            print(f"{t['from']} → {t['to']:<10} {t['change']:>12.2f} {t['percent_change']:>11.2f}% {arrow:>6}")

        print("-" * 55)

    except Exception as e:
        print(f"Unexpected error: {e}")

def prompt_set_budget(user_id):
    """Prompt user for budget info and call the logic layer."""
    category = input("Enter category name: ").strip()
    try:
        limit = float(input("Enter budget limit: "))
        set_budget_limit(user_id, category, limit)
    except ValueError:
        print("Invalid limit. Please enter a number.")

def prompt_check_budget(user_id):
    transactions = load_json(TRANSACTIONS_FILE)
    budgets = load_json(BUDGET_FILE)

    print("\nBudget Status")
    print("-" * 40)
    alerts = check_budget_limits(user_id, transactions, budgets, verbose=True)

    if not alerts:
        print("All budgets are within limits.")

def prompt_set_goal(user_id):
    """Prompt user for goal info and call the logic layer."""
    name = input("Enter goal name: ").strip()
    try:
        amount = float(input("Enter target amount: "))
        set_goal(user_id, name, amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")

def prompt_view_goals(user_id):
    transactions = load_json(TRANSACTIONS_FILE)
    goals = load_json(GOALS_FILE)

    print("\nGoals Progress")
    print("-" * 40)
    progress = check_goals_progress(user_id, transactions, goals)

    if not progress:
        print("No goals found.")
        return

    for g in progress:
        print(
            f"- {g['goal_name']}: {g['progress_percent']}% ({g['status']}) | "
            f"Target: {g['target_amount']} | Remaining: {g['remaining']:.2f}"
        )

def prompt_process_recurring(user_id):
    
    transactions = load_json(TRANSACTIONS_FILE)

    print("\nProcess Recurring Transactions")
    print("-" * 40)

    updated_txns = process_recurring_transactions(user_id, transactions)
    save_json(updated_txns, TRANSACTIONS_FILE)

def prompt_calculate_health(user_id):
    transactions = load_json(TRANSACTIONS_FILE)
    goals = load_json(GOALS_FILE)

    print("\nFinancial Health Score")
    print("-" * 40)

    score, status = calculate_financial_health(user_id, transactions, goals)
    print(f"Your Financial Health Score: {score} ({status})")