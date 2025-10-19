import uuid
import time

def generate_unique_id() -> str:
    """ Generate a unique ID for users. """
    return str(uuid.uuid4())

def generate_transaction_id() -> str:
    """Generate a unique ID for transactions (TXN-<timestamp>-<short-uuid>)."""
    timestamp = int(time.time())
    short_uuid = uuid.uuid4().hex[:6]
    return f"TXN-{timestamp}-{short_uuid}"