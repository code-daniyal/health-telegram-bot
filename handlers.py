
# handlers.py
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from calculations import calculate_bmi, calculate_calories
from database import add_record, get_user_progress
from charts import create_bmi_chart
import os
# --- Главное меню ---
def main_menu():
    keyboard = [
        ["🏋️ Тренировки", "🥗 Питание"],
        ["😴 Сон", "📊 Рассчитать ИМТ"],
        ["🔥 Рассчитать калории", "📈 Мой прогресс"],
        ["❓ Задать вопрос", "ℹ️ О боте"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- Старт ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Healthy Bot 💪\nВыбери раздел:",
        reply_markup=main_menu()
    )

# --- Основной обработчик сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)

    # --- Кнопки ---
    if text == "🏋️ Тренировки":
        await update.message.reply_text("Тренируйся 3-4 раза в неделю 💪")
    elif text == "🥗 Питание":
        await update.message.reply_text("Ешь белок, овощи и фрукты 🥗")
    elif text == "😴 Сон":
        await update.message.reply_text("Спи 8-9 часов 😴")
    elif text == "📊 Рассчитать ИМТ":
        await update.message.reply_text("Напиши вес и рост через пробел\nПример: 70 175")
        context.user_data["mode"] = "bmi"
    elif text == "🔥 Рассчитать калории":
        await update.message.reply_text("Напиши вес(кг) рост(см) возраст\nПример: 70 175 16")
        context.user_data["mode"] = "calories"
    elif text == "📈 Мой прогресс":
        # Получаем данные
        records = get_user_progress(user_id)
        if not records:
            await update.message.reply_text("У тебя пока нет данных.")
            return
        
        # 1️⃣ Отправляем текст с прогрессом
        progress_text = "📈 Твой прогресс:\n\n"
        for i, record in enumerate(records, 1):
            progress_text += f"{i}) Вес: {record['weight']} кг | ИМТ: {record['bmi']}\n"
        await update.message.reply_text(progress_text)

        # 2️⃣ Отправляем график
        chart_file = create_bmi_chart(user_id)
        if chart_file and os.path.exists(chart_file):
            with open(chart_file, "rb") as f:
                await update.message.reply_photo(photo=InputFile(f))
            os.remove(chart_file)  # удаляем файл после отправки
    elif text == "ℹ️ О боте":
        await update.message.reply_text("Healthy Bot 3.0 💪")
    else:
        # --- Обработка режимов ---
        mode = context.user_data.get("mode")
        if mode == "bmi":
            try:
                weight, height_cm = map(float, text.split())
                bmi_value, category, advice = calculate_bmi(weight, height_cm)
                add_record(user_id, weight, height_cm, bmi_value)
                await update.message.reply_text(
                    f"📊 Твой ИМТ: {bmi_value}\n"
                    f"Категория: {category}\n"
                    f"Совет: {advice}\n\n"
                    "Данные сохранены 📁"
                )
            except:
                await update.message.reply_text("Ошибка. Пример: 70 175")
            context.user_data["mode"] = None
        elif mode == "calories":
            try:
                weight, height, age = map(float, text.split())
                calories_needed = calculate_calories(weight, height, age)
                await update.message.reply_text(f"Тебе нужно примерно {calories_needed} ккал в день 🔥")
            except:
                await update.message.reply_text("Ошибка. Пример: 70 175 16")
            context.user_data["mode"] = None
        

# handlers.py
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from calculations import calculate_bmi, calculate_calories
from database import add_record, get_user_progress
from charts import create_bmi_chart
import os
# --- Главное меню ---
def main_menu():
    keyboard = [
        ["🏋️ Тренировки", "🥗 Питание"],
        ["😴 Сон", "📊 Рассчитать ИМТ"],
        ["🔥 Рассчитать калории", "📈 Мой прогресс"],
        ["❓ Задать вопрос", "ℹ️ О боте"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- Старт ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Healthy Bot 💪\nВыбери раздел:",
        reply_markup=main_menu()
    )

# --- Функция для создания графика ---
def create_bmi_chart(user_id):
    records = get_user_progress(user_id)
    if not records:
        return None
    
    labels = list(range(1, len(records)+1))
    bmis = [r['bmi'] for r in records]
    weights = [r['weight'] for r in records]

    plt.figure(figsize=(6,4))
    plt.plot(labels, bmis, marker='o', linestyle='-', color='blue', label='ИМТ')
    plt.plot(labels, weights, marker='s', linestyle='--', color='green', label='Вес')
    plt.title('Прогресс пользователя')
    plt.xlabel('Записи')
    plt.ylabel('Значение')
    plt.grid(True)
    plt.legend()

    filename = f"{user_id}_progress.png"
    plt.savefig(filename)
    plt.close()
    return filename

# --- Основной обработчик сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)

    # --- Кнопки ---
    if text == "🏋️ Тренировки":
        await update.message.reply_text("Тренируйся 3-4 раза в неделю 💪")
    elif text == "🥗 Питание":
        await update.message.reply_text("Ешь белок, овощи и фрукты 🥗")
    elif text == "😴 Сон":
        await update.message.reply_text("Спи 8-9 часов 😴")
    elif text == "📊 Рассчитать ИМТ":
        await update.message.reply_text("Напиши вес и рост через пробел\nПример: 70 175")
        context.user_data["mode"] = "bmi"
    elif text == "🔥 Рассчитать калории":
        await update.message.reply_text("Напиши вес(кг) рост(см) возраст\nПример: 70 175 16")
        context.user_data["mode"] = "calories"
    elif text == "📈 Мой прогресс":
        # Получаем данные
        records = get_user_progress(user_id)
        if not records:
            await update.message.reply_text("У тебя пока нет данных.")
            return
        
        # 1️⃣ Отправляем текст с прогрессом
        progress_text = "📈 Твой прогресс:\n\n"
        for i, record in enumerate(records, 1):
            progress_text += f"{i}) Вес: {record['weight']} кг | ИМТ: {record['bmi']}\n"
        await update.message.reply_text(progress_text)

        # 2️⃣ Отправляем график
        chart_file = create_bmi_chart(user_id)
        if chart_file and os.path.exists(chart_file):
            with open(chart_file, "rb") as f:
                await update.message.reply_photo(photo=InputFile(f))
            os.remove(chart_file)  # удаляем файл после отправки
    elif text == "ℹ️ О боте":
        await update.message.reply_text("Healthy Bot 3.0 💪")
    else:
        # --- Обработка режимов ---
        mode = context.user_data.get("mode")
        if mode == "bmi":
            try:
                weight, height_cm = map(float, text.split())
                bmi_value, category, advice = calculate_bmi(weight, height_cm)
                add_record(user_id, weight, height_cm, bmi_value)
                await update.message.reply_text(
                    f"📊 Твой ИМТ: {bmi_value}\n"
                    f"Категория: {category}\n"
                    f"Совет: {advice}\n\n"
                    "Данные сохранены 📁"
                )
            except:
                await update.message.reply_text("Ошибка. Пример: 70 175")
            context.user_data["mode"] = None
        elif mode == "calories":
            try:
                weight, height, age = map(float, text.split())
                calories_needed = calculate_calories(weight, height, age)
                await update.message.reply_text(f"Тебе нужно примерно {calories_needed} ккал в день 🔥")
            except:
                await update.message.reply_text("Ошибка. Пример: 70 175 16")
            context.user_data["mode"] = None
        else:
            await update.message.reply_text("Я пока не понимаю 😅\nВыбери кнопку из меню.")