import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

SUPER_ADMIN_ID = int(os.getenv("SUPER_ADMIN_ID"))
USERS_FILE = BASE_DIR / "allowed_users.json"
REJECTED_FILE = BASE_DIR / "rejected_requests.json"


def get_allowed_user_ids():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [x["id"] for x in data.get("admins", []) + data.get("users", [])]

def get_admin_ids():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        admins = json.load(f)["admins"]
    return [admin for admin in admins if admin != SUPER_ADMIN_ID]

def get_user_ids():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return [user["id"] for user in json.load(f)["users"]]

def get_all_admins():
    return [SUPER_ADMIN_ID] + get_admin_ids()

def add_user_id(user_id, name):
    with open(USERS_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        if not any(user["id"] == user_id for user in data["users"]):
            data["users"].append({"id": user_id, "name": name})
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()

def remove_user_id(user_id):
    with open(USERS_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        original_len = len(data["users"])
        data["users"] = [u for u in data["users"] if u["id"] != user_id]
        if len(data["users"]) < original_len:
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()


def add_admin_id(user_id, name):
    with open(USERS_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        if not any(admin["id"] == user_id for admin in data["admins"]):
            data["admins"].append({"id": user_id, "name": name})
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()

def remove_admin_id(user_id):
    with open(USERS_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        original_len = len(data["admins"])
        data["admins"] = [a for a in data["admins"] if a["id"] != user_id]
        if len(data["admins"]) < original_len:
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()


def is_super_admin(user_id: int) -> bool:
    return user_id == SUPER_ADMIN_ID


def load_rejected():
    if not REJECTED_FILE.exists():
        return {}
    with open(REJECTED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_rejected(data):
    with open(REJECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def has_exceeded_retries(user_id: int) -> bool:
    data = load_rejected()
    return data.get(str(user_id), 0) >= 3

def increment_reject(user_id: int):
    data = load_rejected()
    data[str(user_id)] = data.get(str(user_id), 0) + 1
    save_rejected(data)


def get_reject_count(user_id: int) -> int:
    data = load_rejected()
    return data.get(str(user_id), 0)


def get_all_users_info():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
