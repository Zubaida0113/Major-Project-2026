import json
import os

STORAGE_FILE = "data/storage.json"

def load_data():
    if not os.path.exists(STORAGE_FILE):
        return {"complaints": [], "users": {}}

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_complaint(complaint):
    data = load_data()
    data["complaints"].append(complaint)
    save_data(data)

def get_user_data(user_id):
    data = load_data()
    return data["users"].get(user_id, {
        "total": 0,
        "valid": 0,
        "false": 0
    })

def update_user(user_id, is_valid=True):
    data = load_data()

    if user_id not in data["users"]:
        data["users"][user_id] = {"total": 0, "valid": 0, "false": 0}

    data["users"][user_id]["total"] += 1

    if is_valid:
        data["users"][user_id]["valid"] += 1
    else:
        data["users"][user_id]["false"] += 1

    save_data(data)