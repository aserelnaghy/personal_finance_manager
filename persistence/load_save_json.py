import json
import os
from utils.errors import DataPersistenceError

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    try:
        with open(file_path, 'r') as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        raise ValueError(f"Error reading JSON from file {file_path}: {e}")

def save_json(data, file_path):

    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except OSError as e:
        raise DataPersistenceError(f"Error saving JSON to {file_path}: {e}")