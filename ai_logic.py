import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем ключи
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Настройка ИИ
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
   model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    print("⚠️ ОШИБКА: GEMINI_API_KEY не найден в .env!")

async def get_ai_answer(question):
    try:
        print(f"🤖 ИИ получил вопрос: {question}") # Увидим это в консоли
        
        prompt = (
            f"Ты — научный ассистент Healthy Bot. Отвечай на русском языке, "
            f"используй научные факты из химии и биологии. Будь краток. "
            f"Вопрос: {question}"
        )
        
        response = model.generate_content(prompt)
        print("✅ ИИ успешно сгенерировал ответ")
        return response.text
    except Exception as e:
        print(f"❌ ОШИБКА ИИ: {e}")
        return "Извини, мой научный модуль сейчас на калибровке. Попробуй позже! 🧪"