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
    return data.get(user_id, [])