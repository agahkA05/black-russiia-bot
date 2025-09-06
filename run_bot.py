import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import os

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

async def main():
    """Главная функция"""
    # Создаем папку для загрузок
    os.makedirs("uploads", exist_ok=True)
    
    # Запускаем бота
    logger.info("Запуск бота...")
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())



