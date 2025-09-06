from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_search_filters_keyboard():
    """Клавиатура фильтров поиска"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="🏷️ По категории", callback_data="filter_category")])
    buttons.append([InlineKeyboardButton(text="💰 По цене", callback_data="filter_price")])
    buttons.append([InlineKeyboardButton(text="🌐 По серверу", callback_data="filter_server")])
    buttons.append([InlineKeyboardButton(text="🔤 По названию", callback_data="filter_title")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_analytics_keyboard():
    """Клавиатура аналитики"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="📈 Продажи", callback_data="analytics_sales")])
    buttons.append([InlineKeyboardButton(text="💰 Цены", callback_data="analytics_prices")])
    buttons.append([InlineKeyboardButton(text="👥 Пользователи", callback_data="analytics_users")])
    buttons.append([InlineKeyboardButton(text="🏷️ Категории", callback_data="analytics_categories")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_notification_settings_keyboard():
    """Клавиатура настроек уведомлений"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="📦 Новые товары", callback_data="notify_new_items")])
    buttons.append([InlineKeyboardButton(text="💬 Сообщения", callback_data="notify_messages")])
    buttons.append([InlineKeyboardButton(text="💰 Скидки", callback_data="notify_discounts")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_servers_keyboard():
    """Клавиатура серверов"""
    from config import SERVERS
    buttons = []
    for i in range(0, len(SERVERS), 2):
        row = []
        for j in range(2):
            if i + j < len(SERVERS):
                row.append(InlineKeyboardButton(text=SERVERS[i + j], callback_data=f"serv_{SERVERS[i + j]}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_sort_options_keyboard():
    """Клавиатура сортировки"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="📅 По дате", callback_data="sort_date")])
    buttons.append([InlineKeyboardButton(text="💰 По цене", callback_data="sort_price")])
    buttons.append([InlineKeyboardButton(text="⭐ По рейтингу", callback_data="sort_rating")])
    buttons.append([InlineKeyboardButton(text="👀 По популярности", callback_data="sort_popularity")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_blacklist_keyboard():
    """Клавиатура черного списка"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="➕ Добавить", callback_data="blacklist_add")])
    buttons.append([InlineKeyboardButton(text="📋 Список", callback_data="blacklist_list")])
    buttons.append([InlineKeyboardButton(text="🗑️ Удалить", callback_data="blacklist_remove")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)