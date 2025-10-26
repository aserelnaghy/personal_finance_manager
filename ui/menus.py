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

