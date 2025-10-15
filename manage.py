
import json
import threading
import datetime
import os

class UserActivityManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.lock = threading.Lock()
        if not os.path.exists(filename):
            self.data = {}
            self._save()
        else:
            self._load()

    def _load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                self.data = json.load(f)
            except:
                self.data = {}

    def _save(self):
        with self.lock:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)

    def add_user(self, user_id):
        uid = str(user_id)
        if uid not in self.data:
            self.data[uid] = {
                "is_loggin": False,
                "email": "",
                "phone": "",
                "join Time": datetime.datetime.now().isoformat(),   # ← تبدیل به رشته
                "Last_activity": datetime.datetime.now().isoformat()  # ← تبدیل به رشته
            }
            self._save()
            
    def set_email(self, user_id, email):
        uid = str(user_id)
        if uid not in self.data:
            self.add_user(user_id)
        self.data[uid]["email"] = email
        self._save()

    def _update_field(self, user_id, field, value, is_numeric=False):
        user_key = str(user_id)
        if user_key not in self.data:
            self.add_user(user_id)
        if is_numeric:
            try:
                value = float(value)
            except:
                value = 0
        self.data[user_key][field] = value
        self.data[user_key]["Last_activity"] = datetime.datetime.now().isoformat()
        self._save()

    # --- متدهای ست کردن فیلدها ---
    def set_first_name(self, user_id, first_name):
        self._update_field(user_id, "first name", first_name)
        
    def set_password(self, user_id, password):
        self._update_field(user_id, "password", password)
        
    def set_phone_number(self, user_id, phone):
        self._update_field(user_id, "phone", phone)

    def set_is_loggin(self, user_id, is_loggin: bool):
        self._update_field(user_id, "is_loggin", bool(is_loggin))

    # --- چک کردن لاگین ---
    def is_loggin(self, user_id):
        user_key = str(user_id)
        if user_key in self.data:
            return bool(self.data[user_key].get("is_loggin", False))
        return False

    # --- گرفتن اطلاعات ---
    def get_user(self, user_id):
        return self.data.get(str(user_id), None)

    def all_users(self):
        return self.data

class BaseManager:
    def __init__(self, filename: str, default_data):
        self.filename = filename
        self.lock = threading.Lock()
        if not os.path.exists(filename):
            self._save(default_data)
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return {"users": []}
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    # اگه لیست بود، تبدیل به دیکشنری با کلید users
                    data = {"users": data}
                elif not isinstance(data, dict):
                    data = {"users": []}
                return data
            except:
                return {"users": []}


    def _save(self, data=None):
        if data is not None:
            self.data = data
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)



class UserManager(BaseManager):
    def __init__(self, filename="control_users.json", phone_file="data.json", limit_file="limits.json",code_file="codes.json"):
        super().__init__(filename, default_data={"users": []})  # ← اینجا
        self.phone_file = phone_file
        self.limit_file = limit_file
        self.code_file = code_file


    # ------------------- User management -------------------

    def _load_codes(self):
        try:
            with open(self.code_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_codes(self, data):
        with open(self.code_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save_code(self, user_id, code):
        data = self._load_codes()
        data[str(user_id)] = str(code)
        self._save_codes(data)

    def get_user_data(self, user_id):
        data = self._load_codes()
        return {"code": data.get(str(user_id))}  # شبیه ساختار قدیم

    def remove_code(self, user_id):
        data = self._load_codes()
        if str(user_id) in data:
            del data[str(user_id)]
            self._save_codes(data)
        user_id = int(user_id)
        users_list = self.data.get("users", [])
        if not any(int(u["id"]) == user_id for u in users_list):
            users_list.append({"id": user_id, "banned": False})
            self.data["users"] = users_list
            self._save()

    def ban_user(self, user_id: int):
        user_id = int(user_id)
        for u in self.data.get("users", []):
            if int(u["id"]) == user_id:
                u["banned"] = True
                self._save()
                return True
        return False

    def unban_user(self, user_id: int):
        user_id = int(user_id)
        for u in self.data.get("users", []):
            if int(u["id"]) == user_id:
                u["banned"] = False
                self._save()
                return True
        return False
    
    def is_banned(self, user_id: int) -> bool:
        user_id = int(user_id)
        return any(int(u["id"]) == user_id and u["banned"] for u in self.data.get("users", []))
    
    def total_users(self) -> int:
        return len(self.data.get("users", []))

    def banned_users(self) -> list:
        return [u for u in self.data.get("users", []) if u["banned"]]
    
    def all_users(self) -> list:
        return self.data.get("users", [])
    