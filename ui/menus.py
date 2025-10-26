from auth.user_manager import get_current_user
from ui.prompts import *
from config import TRANSACTION_FILE, BUDGET_FILE, GOALS_FILE, RECURRING_FILE

# from features.budget_manager import check_budget_limits
# from features.goal_tracker import check_goals_progress
# from features.recurring_processor import process_recurring_transactions
# from features.financial_health import calculate_financial_health

from persistence.load_save_json import load_json

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

    transactions = load_json(TRANSACTION_FILE)

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
    pause() 
