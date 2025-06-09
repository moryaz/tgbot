import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Конфигурация
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Получите у @BotFather
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Получите на openweathermap.org
CITY = "Tver,RU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот погоды для Твери.\n"
        "Используй /weather чтобы узнать текущую погоду."
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем данные о погоде
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()
        
        # Проверка на ошибки API
        if data["cod"] != 200:
            raise Exception(data["message"])
        
        # Парсим данные
        weather_data = {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "description": data["weather"][0]["description"].capitalize(),
            "city": data["name"]
        }
        
        # Формируем ответ
        message = (
            f"🌡 Погода в {weather_data['city']}:\n"
            f"• Температура: {weather_data['temp']}°C\n"
            f"• Ощущается как: {weather_data['feels_like']}°C\n"
            f"• Влажность: {weather_data['humidity']}%\n"
            f"• Ветер: {weather_data['wind']} м/с\n"
            f"• Описание: {weather_data['description']}"
        )
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

def main():
    # Создаем приложение бота
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    
    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()