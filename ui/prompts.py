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


