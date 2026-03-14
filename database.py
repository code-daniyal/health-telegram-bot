
# database.py
import json
import os

FILE_NAME = "data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def add_record(user_id, weight, height, bmi):
    data = load_data()
    if user_id not in data:
        data[user_id] = []
    data[user_id].append({
        "weight": weight,
        "height": height,
        "bmi": bmi
    })
    save_data(data)

def get_user_progress(user_id):
    data = load_data()

import json
import os

FILE_NAME = "data.json"

def load_data():
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
    except Exception as e:
        print(f"Ошибка загрузки JSON: {e}")
    return {}

def save_data(data):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения JSON: {e}")

def add_record(user_id, weight, height, bmi):
    user_id = str(user_id) # Убеждаемся, что ID — строка
    data = load_data()
    if user_id not in data:
        data[user_id] = []
    data[user_id].append({
        "weight": weight,
        "height": height,
        "bmi": bmi
    })
    save_data(data)

def get_user_progress(user_id):
    user_id = str(user_id)
    data = load_data()
    return data.get(user_id, [])