import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    prompt = f"""Ты персональный коуч по здоровью в стиле Whoop. Пиши на русском, используй эмодзи, без звёздочек.

Пользователь прислал данные за день:
{user_text}

Напиши подробный анализ в таком формате:

Привет Виктория! Вот твоя сводка за сегодня 💪

😴 СОН
Показатели: [перечисли цифры из данных]
Анализ: [что означают эти цифры]
Рекомендация: [конкретный совет]

❤️ ПУЛЬС И ВОССТАНОВЛЕНИЕ
Показатели: [перечисли цифры]
Анализ: [что означают]
Рекомендация: [совет]

🏃 АКТИВНОСТЬ
Показатели: [перечисли цифры]
Анализ: [оценка нагрузки]
Рекомендация: [совет]

🥗 ПИТАНИЕ
Показатели: [перечисли цифры]
Анализ: [что не хватает]
Рекомендация: [конкретные продукты]

🌸 ЦИКЛ
Анализ: [как фаза влияет на всё]

📋 ПЛАН НА ЗАВТРА
Тренировка: [коротко]
Питание: [коротко]
Сон: [во сколько лечь]

Пиши конкретно по цифрам которые прислала. Без воды."""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    
    result = response.json()
    answer = result["content"][0]["text"]
    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
