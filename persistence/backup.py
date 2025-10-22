import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import shutil
from datetime import datetime
from utils.errors import DataPersistenceError
from config import BACKUP_DIR, DATA_DIR

def backup_file(file_path, backup_dir=BACKUP_DIR):
    """
    Create a timestamped backup copy of a JSON file before overwrite.

    Returns:
        str: Path to the created backup file.
    Raises:
        DataPersistenceError: If the file does not exist or copying fails.
    """
    try:
        # Check that source file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Source file '{file_path}' does not exist.")

        # Ensure backup directory exists
        os.makedirs(backup_dir, exist_ok=True)

        # Construct backup file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(
            backup_dir,
            f"{os.path.basename(file_path)}_{timestamp}.bak"
        )

        # Copy file safely
        shutil.copy2(file_path, backup_path)
        return backup_path

    except FileNotFoundError as e:
        # Expected: file missing — raise meaningful persistence error
        raise DataPersistenceError(str(e))
    except OSError as e:
        # File system or permission errors
        raise DataPersistenceError(f"Failed to back up '{file_path}': {e}")


# if __name__ == "__main__":
#     # Create dummy data dir
#     os.makedirs(BACKUP_DIR, exist_ok=True)

#     # Create a sample file to back up
#     file_path = DATA_DIR / "test.json"
#     with open(file_path, "w") as f:
#         f.write('{"user_id": "001", "name": "Test User"}')

#     # Try making a backup
#     try:
#         result = backup_file(file_path, BACKUP_DIR)
#         print("Backup successful:", result)
#     except DataPersistenceError as e:
#         print("Backup failed:", e)
