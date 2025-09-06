import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import router
from database import Database

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(router)

# Инициализация базы данных
db = Database("black_russia_market.db")

async def on_startup():
    """Действия при запуске бота"""
    logger.info("Бот запущен!")
    
    # Добавляем базовые интеграции
    integrations = [
        {
            "name": "Официальный чат",
            "url": "https://t.me/black_russia_chat",
            "type": "chat"
        },
        {
            "name": "Официальный сайт",
            "url": "https://blackrussia.com",
            "type": "website"
        },
        {
            "name": "Официальный канал",
            "url": "https://t.me/black_russia_channel",
            "type": "channel"
        }
    ]
    
    for integration in integrations:
        db.add_integration(
            name=integration["name"],
            integration_type=integration["type"],
            url=integration["url"],
            description=""
        )
    
    logger.info("Базовые интеграции добавлены!")

async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("Бот остановлен!")

async def main():
    """Главная функция"""
    # Создаем папку для загрузок
    os.makedirs("uploads", exist_ok=True)
    
    # Регистрация событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Запуск бота в режиме polling
    logger.info("Запуск бота в режиме polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())