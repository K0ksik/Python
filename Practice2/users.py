# users.py
import json
import os
import threading

class Users:
    def __init__(self):
        self.file_path = "notes.json"
        self.lock = threading.Lock()

    def register_user(self, username, password):
        data = self._load_data()
        if username in data:
            print("Пользователь уже существует")
        else:
            data[username] = {"password": password, "notes": []}
            save_thread = threading.Thread(target=self._save_data, args=(data,))
            save_thread.start()
            print("Пользователь зарегистрирован")

    def login_user(self, username, password):
        data = self._load_data()
        return username in data and data[username]["password"] == password

    def add_note(self, username, note):
        data = self._load_data()
        if username in data:
            data[username]["notes"].append(note)
            save_thread = threading.Thread(target=self._save_data, args=(data,))
            save_thread.start()
            print(f"Заметка добавлена")
        else:
            print("Пользователь не найден")

    def get_notes(self, username):
        data = self._load_data()
        return data.get(username, {}).get("notes", [])

    def _load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def _save_data(self, data):
        with self.lock:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)