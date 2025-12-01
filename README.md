# Personal Finance Manager (Python)

A simple command-line personal finance application built with Python that helps users track income, expenses, goals, and budgets efficiently.
It’s lightweight, file-based (using JSON), and focuses on clarity and reliability — perfect for managing your finances without complex databases or dependencies.

---

## Features

- **User Accounts**
  - Create, log in, and log out of user accounts securely.
  - Prevent duplicate usernames.
  - Persist users in `users.json`.

- **Transactions**
  - Add, view, and categorize income and expenses.
  - Validate type, amount, and description.
  - Persist transactions in `transactions.json`.

- **Dashboard**
  - Detects the current month automatically.
  - Displays monthly income, monthly expenses, and overall balance.
  - Clean text-based summary.

- **Budgeting**
  - Set and check budget limits for different categories.

- **Goals**
  - Create financial goals and track progress toward them.

- **Recurring Transactions**
  - Handle automatic monthly transactions like rent or subscriptions.

- **Error Handling**
  - Input checks for invalid types, unsupported entries, and malformed data.

---

## Installation & Setup
**1. Clone the repository**


    git clone https://github.com/yourusername/personal-finance-manager.git 
    
    cd personal-finance-manager

**2. Ensure Python 3.8+ is installed**

    python --version

**3. Run the program**

    python main.py

---

## Example

### Dashboard Summary
```
----------------------------------------
     MONTHLY DASHBOARD (October 2025)
----------------------------------------
Total Income:       5,200 EGP
Total Expenses:     3,850 EGP
Current Balance:    1,350 EGP

Goals:
 - Save for Laptop: 60% complete

Budgets:
 - Food: Within limit
 - Entertainment: Exceeded!
----------------------------------------