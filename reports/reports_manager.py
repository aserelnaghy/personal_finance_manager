
from collections import defaultdict
from persistence.load_save_json import load_json
from config import TRANSACTIONS_FILE
from datetime import datetime 

def generate_dashboard_summary(transactions):
    """Generate a dashboard summary for the current month and overall balance."""
    today = datetime.today()
    current_month = today.strftime("%Y-%m")

    # --- Monthly filtering ---
    monthly_txns = [
        t for t in transactions
        if datetime.strptime(t["date"], "%Y-%m-%d").strftime("%Y-%m") == current_month
    ]

    # --- Monthly totals ---
    total_income = sum(t["amount"] for t in monthly_txns if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in monthly_txns if t["type"] == "expense")
    net_savings = total_income - total_expenses

    # --- Overall current balance (across all transactions) ---
    overall_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    overall_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    current_balance = overall_income - overall_expenses

    # --- Top spending categories for the month ---
    category_totals = defaultdict(float)
    for t in monthly_txns:
        if t["type"] == "expense":
            category_totals[t["category"]] += t["amount"]

    # Sort and get top 3 categories
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]

    # Calculate percentage contribution per category
    top_categories = [
        {
            "category": cat,
            "amount": amt,
            "percent": round((amt / total_expenses * 100), 1) if total_expenses > 0 else 0
        }
        for cat, amt in top_categories
    ]

    # --- Summary structure ---
    summary = {
        "period": today.strftime("%B %Y"),
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "current_balance": current_balance,
        "top_categories": top_categories
    }

    return summary

def generate_monthly_report(transactions):
    monthly_summary = defaultdict(lambda: {"income": 0, "expense": 0})
    for t in transactions:
        month = datetime.strptime(t["date"], "%Y-%m-%d").strftime("%Y-%m")
        monthly_summary[month][t["type"]] += t["amount"]
    return dict(monthly_summary)

def generate_category_breakdown(transactions, type_filter="expense"):
    categories = defaultdict(float)
    for t in transactions:
        if t["type"] == type_filter:
            categories[t["category"]] += t["amount"]
    return dict(categories)

def generate_spending_trends(transactions):
    monthly = generate_monthly_report(transactions)
    months = sorted(monthly.keys())
    trends = []
    for i in range(1, len(months)):
        prev = monthly[months[i - 1]]["expense"]
        current = monthly[months[i]]["expense"]
        change = current - prev
        percent_change = (change / prev * 100) if prev > 0 else 0
        trends.append({
            "from": months[i - 1],
            "to": months[i],
            "change": change,
            "percent_change": round(percent_change, 2)
        })
    return trends
