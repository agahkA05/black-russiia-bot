from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CATEGORIES, SUBCATEGORIES, CURRENCIES, CONDITIONS, CONDITION_NAMES, SERVERS, COMPLAINT_REASONS

def get_main_menu():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти товары"), KeyboardButton(text="📝 Разместить объявление")],
            [KeyboardButton(text="⭐ Избранное"), KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="🔍 Расширенный поиск"), KeyboardButton(text="📊 Аналитика")],
            [KeyboardButton(text="🔔 Уведомления"), KeyboardButton(text="📋 Правила")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="👑 Админ-панель")]
        ],
        resize_keyboard=True,
        row_width=2
    )
    return keyboard

def get_categories_keyboard():
    """Клавиатура категорий"""
    buttons = []
    for key, value in CATEGORIES.items():
        buttons.append([InlineKeyboardButton(text=value, callback_data=f"cat_{key}")])
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_subcategories_keyboard(category):
    """Клавиатура подкатегорий"""
    buttons = []
    for subcat in SUBCATEGORIES.get(category, []):
        buttons.append([InlineKeyboardButton(text=subcat, callback_data=f"sub_{subcat}")])
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_currencies_keyboard():
    """Клавиатура валют"""
    buttons = []
    for currency in CURRENCIES:
        buttons.append([InlineKeyboardButton(text=currency, callback_data=f"curr_{currency}")])
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_conditions_keyboard():
    """Клавиатура состояний"""
    buttons = []
    for key, value in CONDITION_NAMES.items():
        buttons.append([InlineKeyboardButton(text=value, callback_data=f"cond_{key}")])
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_servers_keyboard():
    """Клавиатура серверов"""
    buttons = []
    for i in range(0, len(SERVERS), 2):
        row = []
        for j in range(2):
            if i + j < len(SERVERS):
                row.append(InlineKeyboardButton(text=SERVERS[i + j], callback_data=f"serv_{SERVERS[i + j]}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_complaint_reasons_keyboard():
    """Клавиатура причин жалоб"""
    buttons = []
    for key, value in COMPLAINT_REASONS.items():
        buttons.append([InlineKeyboardButton(text=value, callback_data=f"complaint_{key}")])
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_complaint")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_advertisement_actions(ad_id, is_owner=False, is_favorite=False):
    """Клавиатура действий с объявлением"""
    buttons = []
    
    if is_favorite:
        buttons.append([InlineKeyboardButton(text="💔 Удалить из избранного", callback_data=f"remove_fav_{ad_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="❤️ В избранное", callback_data=f"add_fav_{ad_id}")])
    
    buttons.append([InlineKeyboardButton(text="💬 Написать продавцу", callback_data=f"chat_{ad_id}")])
    buttons.append([InlineKeyboardButton(text="👤 Подписаться", callback_data=f"follow_{ad_id}")])
    buttons.append([InlineKeyboardButton(text="🚨 Пожаловаться", callback_data=f"complain_{ad_id}")])
    
    if is_owner:
        buttons.append([InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_{ad_id}")])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_ads")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_pagination_keyboard(current_page, total_pages, prefix="ads"):
    """Клавиатура пагинации"""
    buttons = []
    
    if current_page > 1:
        buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{prefix}_page_{current_page-1}")])
    
    if current_page < total_pages:
        buttons.append([InlineKeyboardButton(text="Вперед ➡️", callback_data=f"{prefix}_page_{current_page+1}")])
    
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_panel():
    """Админ-панель"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")])
    buttons.append([InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")])
    buttons.append([InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings")])
    buttons.append([InlineKeyboardButton(text="🛡️ Модерация", callback_data="admin_moderation")])
    buttons.append([InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")])
    buttons.append([InlineKeyboardButton(text="🔗 Интеграции", callback_data="admin_integrations")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_favorites_menu():
    """Меню избранного"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="📦 Товары", callback_data="fav_items")])
    buttons.append([InlineKeyboardButton(text="👤 Продавцы", callback_data="fav_sellers")])
    buttons.append([InlineKeyboardButton(text="🏷️ Категории", callback_data="fav_categories")])
    buttons.append([InlineKeyboardButton(text="⚙️ Настройки", callback_data="fav_settings")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

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

def get_rules_keyboard():
    """Клавиатура правил"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="📋 Основные правила", callback_data="rules_main")])
    buttons.append([InlineKeyboardButton(text="💰 Правила торговли", callback_data="rules_trading")])
    buttons.append([InlineKeyboardButton(text="🚫 Запрещенные товары", callback_data="rules_forbidden")])
    buttons.append([InlineKeyboardButton(text="🛡️ Безопасность", callback_data="rules_safety")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_chat_keyboard(ad_id):
    """Клавиатура чата"""
    buttons = []
    buttons.append([InlineKeyboardButton(text="📦 К объявлению", callback_data=f"back_to_ad_{ad_id}")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    
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