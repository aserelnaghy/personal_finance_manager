import os, json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hashlib
from config import DEFAULT_CURRENCY, USERS_FILE, BASE_DIR
from typing import Dict, Any
from persistence.load_save_json import load_json, save_json
from utils.errors import UserAlreadyExistsError, UserNotFoundError, AuthenticationError
from utils.ids import generate_user_id

CURRENT_USER_FILE = os.path.join(BASE_DIR, "data", "current_user.json")

def hash_pin(pin) -> str:
    """Hash a PIN using SHA-256."""
    return hashlib.sha256(pin.encode()).hexdigest()



def create_user(name, pin, currency = DEFAULT_CURRENCY) -> dict:
    users = load_json(USERS_FILE)

    if any(u["name"].lower() == name.lower() for u in users):
        raise UserAlreadyExistsError(f"User '{name}' already exists.")
    
    user = {
        "user_id": generate_user_id(),
        "name": name.strip(),
        "password": hash_pin(pin),
        "currency": currency,
    }

    users.append(user)
    save_json(users, USERS_FILE)

    # Optionally auto-login after creation
    save_json({"user_id": user["user_id"], "name": user["name"]}, CURRENT_USER_FILE)
    return {"user_id": user["user_id"], "name": user["name"], "currency": user["currency"]}



def verify_user(name: str, pin: str) -> Dict[str, Any]:
    """Checks user credentials and logs them in if correct."""
    users = load_json(USERS_FILE)

    for user in users:
        if user["name"].lower() == name.lower() and user["password"] == hash_pin(pin):
            save_json({"user_id": user["user_id"], "name": user["name"]}, CURRENT_USER_FILE)
            return {"user_id": user["user_id"], "name": user["name"], "currency": user["currency"]}

    raise AuthenticationError("Invalid username or PIN.")



def switch_user(user_id: str) -> dict:
    """Switches the active user profile."""
    users = load_json(USERS_FILE)
    user = next((u for u in users if u["user_id"] == user_id), None)

    if not user:
        raise UserNotFoundError("User ID not found.")

    save_json({"user_id": user["user_id"], "name": user["name"]}, CURRENT_USER_FILE)
    return {"user_id": user["user_id"], "name": user["name"]}



def get_current_user() -> dict | None:
    """Returns the active user if logged in, else None."""
    if not os.path.exists(CURRENT_USER_FILE):
        return None

    try:
        with open(CURRENT_USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None



def logout_user():
    """Clears the current user session."""
    if os.path.exists(CURRENT_USER_FILE):
        os.remove(CURRENT_USER_FILE)