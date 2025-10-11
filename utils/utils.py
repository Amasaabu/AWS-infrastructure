import os
from pathlib import Path
import json

def load_value_frm_config(value_to_get: str):
    BASE_DIR = Path(__file__).parent.parent / "config" / "prod.json"
    config_path = BASE_DIR
    try:
        with open(config_path, "r") as f:
            print(f"Loading configuration from {config_path}")
            config = json.load(f)
    except FileNotFoundError as e:
        # Use environment variable as fallback
        print(f"Fallback: Attempting to load {value_to_get} from environment")
        value = os.getenv(value_to_get)
        if value is not None:
            return value
        else:
            raise Exception(f"Failed to load configuration from {config_path} and environment variable {value_to_get} is not set. Error: {e}")
    return config.get(value_to_get)