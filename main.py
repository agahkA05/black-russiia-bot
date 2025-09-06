import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

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

# Создание веб-сервера для Railway
app = web.Application()

# Health check endpoint
async def health_check(request):
    return web.json_response({"status": "ok", "bot": "running"})

app.router.add_get("/health", health_check)
app.router.add_get("/", health_check)

# Настройка webhook handler
webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)
webhook_handler.register(app, path="/webhook")

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
    
    # Получаем порт от Render
    port = int(os.environ.get("PORT", 8000))
    
    # Запуск веб-сервера
    setup_application(app, dp, bot=bot)
    
    logger.info(f"Запуск веб-сервера на порту {port}")
    await web._run_app(app, port=port)

if __name__ == "__main__":
    asyncio.run(main())