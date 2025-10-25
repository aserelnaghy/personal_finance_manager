
from collections import defaultdict
import datetime 

def generate_dashboard_summary(transactions):
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    net_savings = total_income - total_expenses

    summary = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
    }
    return summary

# def generate_monthly_report(transactions, month, year):
    # monthly_transactions = [
        # t for t in transactions if t["date"].month == month and t["date"].year == year
    # ]
    # report = {
        # "month": month,
        # "year": year,
        # "transactions": monthly_transactions,
        # "summary": generate_dashboard_summary(monthly_transactions),
    # }
    # return report


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
