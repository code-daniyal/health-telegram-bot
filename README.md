# 🥗 AI Healthy Bot

An intelligent Telegram assistant for personalized health tracking and metrics calculation, powered by Large Language Models (LLM).

## 🚀 Key Features
- **AI-Powered Advice:** Real-time health consultations using Llama 3.1 (Groq API).
- **Metric Tracking:** Automated BMI calculation and weight history management.
- **Data Persistence:** User history stored in JSON format for progress tracking.
- **Visual Analytics:** Health charts generated via Matplotlib.

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **Framework:** python-telegram-bot
- **AI Model:** Llama 3.1 (Groq Cloud)
- **Data Visualization:** Matplotlib
- **Web Server:** Flask (for Render.com 24/7 hosting)

## 📦 Installation & Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file with your `TOKEN` and `GROQ_API_KEY`.
4. Run: `python main.py`.

## 🌍 Deployment
The bot is optimized for cloud deployment on **Render** with a built-in health-check system to ensure 24/7 availability.



