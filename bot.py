import os
import json
import requests
from flask import Flask, request

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
CHAT_ID = "376798209"

app = Flask(__name__)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def ask_claude(data_text):
    prompt = "Ты персональный коуч по здоровью в стиле Whoop. Пиши на русском, используй эмодзи, без звёздочек. Используй ТОЛЬКО реальные цифры из данных ниже, ничего не выдумывай. Реальные данные Виктории из Apple Health: " + data_text + " Напиши сводку: Привет Виктория! Вот твоя сводка. Блоки: СОН с показателями и анализом, ПУЛЬС И ВОССТАНОВЛЕНИЕ, АКТИВНОСТЬ, СОСТАВ ТЕЛА с весом и жиром, ПИТАНИЕ, ЦИКЛ с фазой и рекомендациями, ПЛАН НА ЗАВТРА, ИНСАЙТ ДНЯ."

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["content"][0]["text"]

@app.route("/health", methods=["POST"])
def health_data():
    data = request.json
    data_text = json.dumps(data, ensure_ascii=False)
    answer = ask_claude(data_text)
    send_telegram(answer)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Health Bot is running!", 200

if name == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, threaded=True)
