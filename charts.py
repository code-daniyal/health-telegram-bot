
# charts.py
import matplotlib.pyplot as plt
from database import get_user_progress

def create_bmi_chart(user_id):
    records = get_user_progress(user_id)
    if not records:
        return None  # Нет данных
    
    weights = [r['weight'] for r in records]
    bmis = [r['bmi'] for r in records]
    labels = list(range(1, len(records)+1))  # номера записей
    
    plt.figure(figsize=(6,4))
    plt.plot(labels, bmis, marker='o', linestyle='-', color='blue', label='ИМТ')
    plt.plot(labels, weights, marker='s', linestyle='--', color='green', label='Вес')
    
    plt.title('Прогресс пользователя')
    plt.xlabel('Записи')
    plt.ylabel('Значение')
    plt.legend()
    plt.grid(True)
    
    # Сохраняем график во временный файл
    filename = f"{user_id}_progress.png"
    plt.savefig(filename)
    plt.close()

# charts.py
import matplotlib.pyplot as plt
from database import get_user_progress

def create_bmi_chart(user_id):
    records = get_user_progress(user_id)
    if not records:
        return None  # Нет данных
    
    weights = [r['weight'] for r in records]
    bmis = [r['bmi'] for r in records]
    labels = list(range(1, len(records)+1))  # номера записей
    
    plt.figure(figsize=(6,4))
    plt.plot(labels, bmis, marker='o', linestyle='-', color='blue', label='ИМТ')
    plt.plot(labels, weights, marker='s', linestyle='--', color='green', label='Вес')
    
    plt.title('Прогресс пользователя')
    plt.xlabel('Записи')
    plt.ylabel('Значение')
    plt.legend()
    plt.grid(True)
    
    # Сохраняем график во временный файл
    filename = f"{user_id}_progress.png"
    plt.savefig(filename)
    plt.close()
    return filename