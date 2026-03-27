import os
import threading
import sys
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message
from dotenv import load_dotenv

load_dotenv()

# --- БЛОК ДЛЯ RENDER ---
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is alive and kicking!", 200

def run_flask():
    # Render использует 10000 по умолчанию, если переменная не задана
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask запущен на порту {port}", flush=True)
    web_app.run(host='0.0.0.0', port=port)

# -----------------------

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: TOKEN не найден!", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    # 1. Сначала запускаем Flask в потоке
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.setDaemon(True) # Старый добрый способ
    flask_thread.start()

    # 2. Создаем приложение бота
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот начинает Polling... 🚀", flush=True)
    
    try:
        # 3. Запускаем бота в основном потоке
        app.run_polling(drop_pending_updates=True) 
    except Exception as e:
        print(f"💥 Бот упал с ошибкой: {e}", file=sys.stderr)
        sys.exit(1) # Принудительно выходим, чтобы Render увидел краш и перезапустил всё