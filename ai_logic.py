import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Инициализация клиента Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_answer(question):
    try:
        # Используем современную модель Llama-3.3
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Ты — помощник в Healthy Bot. Помогаешь пользователю с вопросами по химии, биологии и здоровью. Отвечай кратко и только на русском языке."},
                {"role": "user", "content": question}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Ошибка Groq: {e}")
        return "Мой научный модуль на калибровке. Попробуй через минуту! 🧪"