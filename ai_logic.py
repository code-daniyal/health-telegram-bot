import os
from groq import Groq
from dotenv import load_dotenv
import sys # Добавили импорт sys

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_answer(question):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Ты — помощник в Healthy Bot. Отвечай кратко на русском."},
                {"role": "user", "content": question}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Это заставит ошибку ПОЯВИТЬСЯ в логах Render
        print(f"❌ Ошибка Groq: {e}", file=sys.stderr, flush=True)
        return f"Ошибка: {e}" # Бот прямо в Телеграме напишет, что не так