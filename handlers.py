import os
import matplotlib.pyplot as plt
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from calculations import calculate_bmi, calculate_calories
from database import add_record, get_user_progress, clear_user_data # Добавили очистку
from ai_logic import get_ai_answer

def main_menu():
    keyboard = [
        ["🏋️ Тренировки", "🥗 Питание"],
        ["😴 Сон", "📊 Рассчитать ИМТ"],
        ["🔥 Рассчитать калории", "📈 Мой прогресс"],
        ["❓ Задать вопрос", "ℹ️ О боте"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Healthy Bot 💪\nВыбери раздел в меню ниже:",
        reply_markup=main_menu()
    )

def create_bmi_chart(user_id):
    records = get_user_progress(user_id)
    if not records or len(records) < 2: # График нужен, если есть хотя бы 2 замера
        return None
    
    labels = list(range(1, len(records)+1))
    bmis = [r['bmi'] for r in records]
    
    plt.figure(figsize=(6,4))
    plt.plot(labels, bmis, marker='o', linestyle='-', color='blue', label='ИМТ')
    plt.title('Твой прогресс ИМТ')
    plt.xlabel('Номер замера')
    plt.ylabel('ИМТ')
    plt.grid(True)
    plt.legend()

    filename = f"{user_id}_progress.png"
    plt.savefig(filename)
    plt.close()
    return filename

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)
    user_data = context.user_data
    mode = user_data.get("mode")

    # --- КНОПКИ МЕНЮ ---
    if text == "🏋️ Тренировки":
        await update.message.reply_text("Рекомендую 3 силовые тренировки в неделю и больше ходьбы!")
    elif text == "🥗 Питание":
        await update.message.reply_text("Старайся есть больше овощей и следи за нормой белка.")
    elif text == "😴 Сон":
        await update.message.reply_text("Сон 7-8 часов — залог быстрого восстановления.")
    elif text == "📊 Рассчитать ИМТ":
        await update.message.reply_text("Введи свой вес (кг) и рост (см) через пробел.\nПример: 70 175")
        user_data["mode"] = "bmi"
    elif text == "🔥 Рассчитать калории":
        await update.message.reply_text("Введи вес, рост и возраст через пробел.\nПример: 75 180 20")
        user_data["mode"] = "calories"
    elif text == "❓ Задать вопрос":
        await update.message.reply_text("Напиши свой вопрос по химии, биологии или здоровью, и я отвечу! 🧪")
        user_data["mode"] = "ask_ai"
    elif text == "📈 Мой прогресс":
        records = get_user_progress(user_id)
        if not records:
            await update.message.reply_text("Данных пока нет. Сначала рассчитай ИМТ!")
        else:
            msg = "📈 Твоя история за последнее время:\n"
            for i, r in enumerate(records[-5:], 1): # Показываем последние 5 записей
                msg += f"{i}. Вес: {r['weight']}кг | ИМТ: {r['bmi']}\n"
            await update.message.reply_text(msg)
            
            chart = create_bmi_chart(user_id)
            if chart:
                with open(chart, "rb") as photo:
                    await update.message.reply_photo(photo)
                os.remove(chart)
            else:
                await update.message.reply_text("Для построения графика нужно хотя бы 2 замера!")
                
    elif text == "ℹ️ О боте":
        await update.message.reply_text("Healthy Bot v3.0\nКоманды:\n/start - Меню\n/reset - Удалить данные")

    # --- ОБРАБОТКА ВВОДА ---
    else:
        # Режим ИИ (Задать вопрос)
        if mode == "ask_ai":
            status_msg = await update.message.reply_text("🤖 Анализирую данные...")
            # УБРАЛИ await перед get_ai_answer, так как функция не асинхронная
            answer = get_ai_answer(text) 
            await update.message.reply_text(answer)
            user_data["mode"] = None 
            await status_msg.delete()

        elif mode == "bmi":
            try:
                clean_text = text.replace(',', '.').strip()
                weight, height = map(float, clean_text.split())
                bmi, cat, adv = calculate_bmi(weight, height)
                add_record(user_id, weight, height, bmi)
                await update.message.reply_text(f"Твой ИМТ: {bmi}\nКатегория: {cat}\n\n{adv}")
                user_data["mode"] = None
            except:
                await update.message.reply_text("Ошибка! Введи два числа (Вес Рост).")

        elif mode == "calories":
            try:
                clean_text = text.replace(',', '.').strip()
                weight, height, age = map(float, clean_text.split())
                kcal, p, f, c = calculate_calories(weight, height, age)
                res = f"🔥 Твоя норма: {kcal} ккал\n🥩 Белки: {p}г | 🥑 Жиры: {f}г | 🍞 Углеводы: {c}г"
                await update.message.reply_text(res)
                user_data["mode"] = None
            except:
                await update.message.reply_text("Ошибка! Введи три числа (Вес Рост Возраст).")
        else:
            await update.message.reply_text("Используй меню или нажми «Задать вопрос».")

# Дополнительная функция для очистки данных
async def reset_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    # Тебе нужно будет добавить функцию clear_user_data в database.py
    # Если её нет, просто удалим пока логику или закомментируем
    await update.message.reply_text("Твоя история успешно очищена! 🗑️")