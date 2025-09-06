import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8172843951:AAFHMnhFITsIlnA9EwgpVenTHg47UO64bys"

# Инициализация базы данных
def init_database():
    conn = sqlite3.connect('black_russia_market.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS advertisements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            price REAL,
            currency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_main_menu():
    """Главное меню"""
    keyboard = [
        [KeyboardButton("🔍 Найти товары"), KeyboardButton("📝 Разместить объявление")],
        [KeyboardButton("⭐ Избранное"), KeyboardButton("👤 Профиль")],
        [KeyboardButton("📋 Правила"), KeyboardButton("❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    
    # Добавляем пользователя в базу
    conn = sqlite3.connect('black_russia_market.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(
        "🎮 **Добро пожаловать в Black Russia Bot!**\n\n"
        "Здесь ты можешь покупать и продавать игровые предметы!\n\n"
        "**Выбери действие:**",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

async def search_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск товаров"""
    conn = sqlite3.connect('black_russia_market.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, u.username
        FROM advertisements a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.is_active = TRUE
        ORDER BY a.created_at DESC
        LIMIT 10
    ''')
    
    ads = cursor.fetchall()
    conn.close()
    
    if not ads:
        await update.message.reply_text("📭 Пока нет объявлений. Будь первым!")
        return
    
    text = "🔍 **Найденные товары:**\n\n"
    for i, ad in enumerate(ads, 1):
        text += f"**{i}.** 📦 **{ad[2]}**\n"
        text += f"💰 Цена: {ad[4]} {ad[5]}\n"
        text += f"👤 Продавец: @{ad[7] or 'Не указан'}\n"
        text += f"🕒 {ad[6]}\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def create_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание объявления"""
    await update.message.reply_text(
        "📝 **Создание объявления**\n\n"
        "Для создания объявления используй команду /create_ad\n"
        "Или напиши мне в личные сообщения!",
        parse_mode='Markdown'
    )

async def favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Избранное"""
    await update.message.reply_text("⭐ **Избранное**\n\nПока пусто. Добавь товары в избранное!")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Профиль пользователя"""
    user_id = update.effective_user.id
    
    conn = sqlite3.connect('black_russia_market.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM advertisements WHERE user_id = ? AND is_active = TRUE', (user_id,))
    ads_count = cursor.fetchone()[0]
    
    conn.close()
    
    text = f"👤 **Твой профиль**\n\n"
    text += f"🆔 ID: {user_id}\n"
    text += f"📝 Объявлений: {ads_count}\n"
    text += f"⭐ Рейтинг: 5.0\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Правила"""
    text = "📋 **Правила Black Russia Bot**\n\n"
    text += "1. 🚫 Запрещены мошенничество и обман\n"
    text += "2. 📸 Обязательно прикрепляй фото товара\n"
    text += "3. 💰 Указывай реальную цену\n"
    text += "4. 🏷️ Правильно выбирай категорию\n"
    text += "5. 👤 Не создавай фейковые аккаунты\n\n"
    text += "**Нарушение правил = бан! ⚠️**"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    text = "❓ **Помощь**\n\n"
    text += "🔍 **Найти товары** - просмотр объявлений\n"
    text += "📝 **Разместить объявление** - создать новое\n"
    text += "⭐ **Избранное** - сохраненные товары\n"
    text += "👤 **Профиль** - твоя статистика\n"
    text += "📋 **Правила** - правила использования\n\n"
    text += "**По вопросам: @Aga_05**"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех остальных сообщений"""
    await update.message.reply_text("Не понимаю. Используй кнопки меню! 🤔")

def main():
    """Главная функция"""
    # Инициализация базы данных
    init_database()
    
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^🔍 Найти товары$"), search_items))
    application.add_handler(MessageHandler(filters.Regex("^📝 Разместить объявление$"), create_ad))
    application.add_handler(MessageHandler(filters.Regex("^⭐ Избранное$"), favorites))
    application.add_handler(MessageHandler(filters.Regex("^👤 Профиль$"), profile))
    application.add_handler(MessageHandler(filters.Regex("^📋 Правила$"), rules))
    application.add_handler(MessageHandler(filters.Regex("^❓ Помощь$"), help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запуск бота
    print("Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()