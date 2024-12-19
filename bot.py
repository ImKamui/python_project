import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, KeyboardButton, ContentType
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from geopy.distance import geodesic
from database import SessionLocal
from models import Event

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN", "8182443228:AAGznPxs3-VV3LpeAcwKSHXKc8HvvPOqcqU")
if not TOKEN:
    raise ValueError("Не удалось получить токен. Убедитесь, что переменная окружения TOKEN установлена.")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def welcome(message: Message):
    """Приветственное сообщение с запросом на отправку геолокации"""
    await message.answer(
        "Добро пожаловать! Поделитесь геолокацией, чтобы мы могли найти ближайшие мероприятия не только по времени, но и по месту.",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]],
            resize_keyboard=True
        )
    )

@dp.message(lambda message: message.location is not None)
async def handle_location(message: Message): 
    """Обработка геолокации пользователя и поиск ближайших мероприятий"""
    user_lat = message.location.latitude
    user_lon = message.location.longitude
    logging.info("Получена геолокация от пользователя.")
    logging.info(f"Широта: {user_lat}, Долгота: {user_lon}")

    session = SessionLocal()
    try: 
        events = session.query(Event).all()
        response = "🎉 Ближайшие мероприятия в радиусе 10 км:\n\n"
        count = 0

        for event in events:
            if event.latitude and event.longitude:
                event_coords = (event.latitude, event.longitude)
                user_coords = (user_lat, user_lon)
                distance = geodesic(user_coords, event_coords).kilometers
                if distance <= 10:
                    event_time = event.time if event.time else "Время уточняется"
                    response += f"📍 {event.title} ({event.location}) - {event_time}\n"
                    count += 1

        if count == 0:
            response += "😔 Мероприятий поблизости не найдено."
        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка при обработке геолокации: {e}")
        await message.answer("Произошла ошибка при поиске мероприятий. Попробуйте ещё раз позже.")
    finally:
        session.close()

@dp.message(Command("events"))
async def send_upcoming_events(message: Message):
    """Показываем ближайшие мероприятия по времени (если геолокация недоступна)"""
    session = SessionLocal()
    try:
        events = session.query(Event).order_by(Event.time).limit(5).all()
        response = "🎉 Ближайшие мероприятия по времени:\n\n"

        if not events:
            response += "😔 Пока мероприятий не найдено."
        else:
            for event in events:
                event_time = event.time if event.time else "Время уточняется"
                response += f"📍 {event.title} ({event.location}) - {event_time}\n"

        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка при получении списка мероприятий: {e}")
        await message.answer("Произошла ошибка при получении списка мероприятий. Попробуйте ещё раз позже.")
    finally:
        session.close()

async def main():
    """Основная точка входа для запуска бота"""
    try:
        logging.info("Запуск бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Произошла критическая ошибка: {e}")
    finally:
        logging.info("Бот был остановлен.")

if __name__ == "__main__":
    asyncio.run(main())




