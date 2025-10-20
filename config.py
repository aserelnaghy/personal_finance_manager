"""
config.py
Global configuration settings for the Personal Finance Manager project.
All paths and constants defined here are imported across modules.
"""

from pathlib import Path
import os

# -------------------------------
# Environment and base paths
# -------------------------------

# Root directory (auto-detect project root)
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / 'data'
BACKUP_DIR = DATA_DIR / 'backups'

#File Names
USERS_FILE = DATA_DIR / 'users.json'
TRANSACTIONS_FILE = DATA_DIR / 'transactions.json'

#Ensure data directories exist
os.makedirs(DATA_DIR, exist_ok=True) # Create data directory if it doesn't exist
os.makedirs(BACKUP_DIR, exist_ok=True) # Create backup directory if it doesn't exist

# -------------------------------
# Application settings
# -------------------------------
APP_NAME = "Personal Finance Manager"
APP_VERSION = "1.0"
DEFAULT_CURRENCY = "EGP"
DATE_FORMAT = "%Y-%m-%d"  # ISO standard
AUTO_BACKUP_LIMIT = 5     # keep last 5 backups

# -------------------------------
# Feature flags
# -------------------------------

ENABLE_RECURRING = True
ENABLE_BUDGETS = True
ENABLE_GOALS = True
