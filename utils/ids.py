import uuid
import time

def generate_user_id() -> str:
    """ Generate a unique ID for users. """
    short_uuid = uuid.uuid4().hex[:6]
    return f"USR-{short_uuid}"

def generate_transaction_id() -> str:
    """Generate a unique ID for transactions (TXN-<short-uuid>)."""
    short_uuid = (uuid.uuid4().hex[:6])
    return f"TXN-{short_uuid}"

# if __name__ == "__main__":
    # print("Unique User ID:", generate_user_id())
    # print("Unique Transaction ID:", generate_transaction_id())