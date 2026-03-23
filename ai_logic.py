import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

# Загружаем ключи из .env
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

model = None

def initialize_ai():
    global model
    if not GEMINI_KEY:
        print("⚠️ ОШИБКА: GEMINI_API_KEY не найден в .env!")
        return

    try:
        genai.configure(api_key=GEMINI_KEY)
        
        priority_models = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-8b',  # Добавили мини-версию
            'gemini-1.5-pro',       # Добавили тяжелую версию
            'gemini-1.0-pro',
            'text-embedding-004'    # Иногда это помогает "пробить" соединение
        ]        
        print("🔍 Калибровка научного модуля...")
        
        for m_name in priority_models:
            try:
                test_model = genai.GenerativeModel(m_name)
                # Проверочный микро-запрос, чтобы убедиться, что квота не 0
                test_model.generate_content("🧪", generation_config={"max_output_tokens": 1})
                model = test_model
                print(f"✅ УСПЕХ: Подключена модель {m_name}")
                return
            except Exception as e:
                print(f"⚠️ Модель {m_name} недоступна или лимит исчерпан. Пробую следующую...")
                continue
        
        print("❌ Не удалось найти доступную модель с текущими лимитами.")
    except Exception as e:
        print(f"⚠️ Ошибка настройки ИИ: {e}")

# Запускаем инициализацию при импорте файла
initialize_ai()

async def get_ai_answer(question):
    if not model:
        return "Мой научный модуль сейчас на калибровке. Попробуй через пару минут! 🧪"
        
    try:
        print(f"🤖 ИИ анализирует вопрос: {question}")
        
        # Промпт, который заставляет ИИ быть кратким (экономим токены/квоту)
        prompt = (
            f"Ты — научный ассистент Healthy Bot. Отвечай кратко, "
            f"используй научные факты. Вопрос: {question}"
        )
        
        # Выполняем запрос в отдельном потоке, чтобы не блокировать бота
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        
        print("✅ Ответ получен")
        return response.text
    except Exception as e:
        print(f"❌ ОШИБКА ГЕНЕРАЦИИ: {e}")
        if "429" in str(e):
            return "Слишком много запросов! Дай мне отдохнуть 60 секунд. 🧬"
        return "Произошла ошибка при анализе. Попробуй еще раз! 🧬"