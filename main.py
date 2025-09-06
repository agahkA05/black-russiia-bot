import logging
import sqlite3
import requests
import json
import time
import threading

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8172843951:AAFHMnhFITsIlnA9EwgpVenTHg47UO64bys"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

def send_message(chat_id, text, reply_markup=None):
    """Отправка сообщения"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(url, data=data)
    return response.json()

def get_main_menu():
    """Главное меню"""
    return {
        'keyboard': [
            [{'text': '🔍 Найти товары'}, {'text': '📝 Разместить объявление'}],
            [{'text': '⭐ Избранное'}, {'text': '👤 Профиль'}],
            [{'text': '📋 Правила'}, {'text': '❓ Помощь'}]
        ],
        'resize_keyboard': True
    }

def handle_start(chat_id, user_id, username, first_name, last_name):
    """Обработчик команды /start"""
    # Добавляем пользователя в базу
    conn = sqlite3.connect('black_russia_market.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()
    
    text = "🎮 **Добро пожаловать в Black Russia Bot!**"
    
    send_message(chat_id, text, get_main_menu())

def handle_search_items(chat_id):
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
        send_message(chat_id, "📭 Пока нет объявлений. Будь первым!")
        return
    
    text = "🔍 **Найденные товары:**\n\n"
    for i, ad in enumerate(ads, 1):
        text += f"**{i}.** 📦 **{ad[2]}**\n"
        text += f"💰 Цена: {ad[4]} {ad[5]}\n"
        text += f"👤 Продавец: @{ad[7] or 'Не указан'}\n"
        text += f"🕒 {ad[6]}\n\n"
    
    send_message(chat_id, text)

def handle_create_ad(chat_id):
    """Создание объявления"""
    text = ("📝 **Создание объявления**\n\n"
            "Для создания объявления используй команду /create_ad\n"
            "Или напиши мне в личные сообщения!")
    send_message(chat_id, text)

def handle_favorites(chat_id):
    """Избранное"""
    send_message(chat_id, "⭐ **Избранное**\n\nПока пусто. Добавь товары в избранное!")

def handle_profile(chat_id, user_id):
    """Профиль пользователя"""
    conn = sqlite3.connect('black_russia_market.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM advertisements WHERE user_id = ? AND is_active = TRUE', (user_id,))
    ads_count = cursor.fetchone()[0]
    
    conn.close()
    
    text = (f"👤 **Твой профиль**\n\n"
            f"🆔 ID: {user_id}\n"
            f"📝 Объявлений: {ads_count}\n"
            f"⭐ Рейтинг: 5.0\n")
    
    send_message(chat_id, text)

def handle_rules(chat_id):
    """Правила"""
    text = ("📋 **Правила Black Russia Bot**\n\n"
            "1. 🚫 Запрещены мошенничество и обман\n"
            "2. 📸 Обязательно прикрепляй фото товара\n"
            "3. 💰 Указывай реальную цену\n"
            "4. 🏷️ Правильно выбирай категорию\n"
            "5. 👤 Не создавай фейковые аккаунты\n\n"
            "**Нарушение правил = бан! ⚠️**")
    
    send_message(chat_id, text)

def handle_help(chat_id):
    """Помощь"""
    text = ("❓ **Помощь**\n\n"
            "Используй кнопки меню для навигации.\n\n"
            "**По вопросам: @Aga_05**")
    
    send_message(chat_id, text)

def handle_message(update):
    """Обработка сообщения"""
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id')
    user = message.get('from', {})
    user_id = user.get('id')
    username = user.get('username')
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    text = message.get('text', '')
    
    if not chat_id or not user_id:
        return
    
    if text == '/start':
        handle_start(chat_id, user_id, username, first_name, last_name)
    elif text == '🔍 Найти товары':
        handle_search_items(chat_id)
    elif text == '📝 Разместить объявление':
        handle_create_ad(chat_id)
    elif text == '⭐ Избранное':
        handle_favorites(chat_id)
    elif text == '👤 Профиль':
        handle_profile(chat_id, user_id)
    elif text == '📋 Правила':
        handle_rules(chat_id)
    elif text == '❓ Помощь':
        handle_help(chat_id)
    else:
        send_message(chat_id, "Не понимаю. Используй кнопки меню! 🤔")

def get_updates(offset=None):
    """Получение обновлений"""
    url = f"{BASE_URL}/getUpdates"
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        logger.error(f"Ошибка получения обновлений: {e}")
        return {'ok': False, 'result': []}

def bot_loop():
    """Основной цикл бота"""
    offset = None
    logger.info("Бот запущен!")
    
    # Ждем подключения к сети
    logger.info("Ожидание подключения к сети...")
    time.sleep(10)
    
    while True:
        try:
            updates = get_updates(offset)
            
            if updates.get('ok'):
                for update in updates.get('result', []):
                    handle_message(update)
                    offset = update.get('update_id', 0) + 1
            else:
                logger.warning(f"Ошибка получения обновлений: {updates}")
                time.sleep(10)
                
        except Exception as e:
            logger.error(f"Ошибка в основном цикле: {e}")
            time.sleep(10)

def main():
    """Главная функция"""
    # Инициализация базы данных
    init_database()
    
    # Запуск бота
    bot_loop()

if __name__ == '__main__':
    main()