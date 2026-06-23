import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".tervault"
CONFIG_FILE = CONFIG_DIR / "config.json"

def save_api_key(api_key):
    """احفظ API key"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": api_key}, f)

    print("✓ API key saved")

def get_api_key():
    """اقرأ API key"""
    if not CONFIG_FILE.exists():
        return None

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    return config.get("api_key")

#if __name__ == "__main__":
 ### print(get_api_key())
