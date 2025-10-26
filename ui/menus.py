from auth.user_manager import get_current_user
from ui.prompts import *
from config import TRANSACTIONS_FILE, BUDGET_FILE, GOALS_FILE, RECURRING_FILE
from persistence.load_save_json import load_json, save_json
import os

# ========== Utility Functions ==========

def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title}".center(50))
    print("=" * 50)

# ========== Transaction Menu ==========

def transactions_menu():
    user = get_current_user()
    if not user:
        print("Please log in first.")
        return

    while True:
        print_header("TRANSACTION MANAGEMENT")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Search/Filter Transactions")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            prompt_add_transaction()
        elif choice == "2":
            prompt_view_transaction()
        elif choice == "3":
            prompt_edit_transactions()
        elif choice == "4":
            prompt_delete_transactions()
        elif choice == "5":
            prompt_search_transactions()
        elif choice == "6":
            break
        else:
            print("Invalid option.")
        pause()


# ========== Reports Menu ==========

def reports_menu():
    user = get_current_user()
    if not user:
        print("Please log in first.")
        return

    transactions = load_json(TRANSACTIONS_FILE)

    while True:
        print_header("REPORTS")
        print("1. Dashboard Summary")
        print("2. Monthly Report")
        print("3. Category Breakdown")
        print("4. Spending Trends")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            prompt_dashboard_summary()
        elif choice == "2":
            prompt_monthly_report()
        elif choice == "3":
            prompt_category_breakdown()
        elif choice == "4":
            prompt_spending_trends()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
        pause()

# ========== Help Menu ==========

def help_menu():
    print_header("HELP & INSTRUCTIONS")
    print("""
Welcome to the Personal Finance Manager!

This application helps you manage your finances in four key areas:
1. User Management — Create, login, and switch between users.
2. Transactions — Add, view, edit, delete, and search transactions.
3. Reports — View summaries and trends of your spending.
4. Advanced Features — Manage budgets, goals, and recurring entries.

Tips:
* Always login before performing transactions.
* Data is stored in JSON files under the 'data/' folder.
* Use Ctrl+C to safely exit the application anytime.
""")

# ========== Advanced Features Menu ==========

def advanced_features_menu():
    """Main advanced features menu for budgets, goals, recurring txns, etc."""
    user = get_current_user()
    if not user:
        print("Please log in first.")
        return

    user_id = user["user_id"]

    # Ensure all data files exist
    for file in [TRANSACTIONS_FILE, BUDGET_FILE, GOALS_FILE, RECURRING_FILE]:
        if not os.path.exists(file):
            print(f"{file} missing — creating a new one.")
            save_json({}, file if "transactions" not in file else [])

    while True:
        print_header("ADVANCED FEATURES")
        print("1. Set Budget Limit")
        print("2. Check Budget Limits")
        print("3. Set Goal")
        print("4. View Goals Progress")
        print("5. Process Recurring Transactions")
        print("6. Calculate Financial Health Score")
        print("7. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            prompt_set_budget(user_id)
        elif choice == "2":
            prompt_check_budget(user_id)
        elif choice == "3":
            prompt_set_goal(user_id)
        elif choice == "4":
            prompt_view_goals(user_id)
        elif choice == "5":
            prompt_process_recurring(user_id)
        elif choice == "6":
            prompt_calculate_health(user_id)
        elif choice == "7":
            break
        else:
            print("Invalid choice, try again.")
        pause()
