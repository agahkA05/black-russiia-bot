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
    for category_id, category_name in CATEGORIES.items():
        buttons.append([InlineKeyboardButton(text=category_name, callback_data=f"category_{category_id}")])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_subcategories_keyboard(category):
    """Клавиатура подкатегорий"""
    if category not in SUBCATEGORIES:
        return get_categories_keyboard()
    
    buttons = []
    for sub in SUBCATEGORIES[category]:
        buttons.append([InlineKeyboardButton(text=sub, callback_data=f"subcategory_{category}_{sub}")])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад к категориям", callback_data="back_to_categories")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_currency_keyboard():
    """Клавиатура выбора валюты"""
    buttons = []
    for currency in CURRENCIES:
        buttons.append([InlineKeyboardButton(text=currency, callback_data=f"currency_{currency}")])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_condition_keyboard():
    """Клавиатура выбора состояния товара"""
    buttons = []
    for condition in CONDITIONS:
        buttons.append([InlineKeyboardButton(text=CONDITION_NAMES[condition], callback_data=f"condition_{condition}")])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_advertisement_actions(ad_id, is_favorite=False, can_delete=False, category="", subcategory="", current_index=0, total_count=1):
    """Действия с объявлением"""
    buttons = []
    
    # Избранное
    if is_favorite:
        buttons.append([InlineKeyboardButton(text="💔 Убрать из избранного", callback_data=f"remove_favorite_{ad_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="❤️ В избранное", callback_data=f"add_favorite_{ad_id}")])
    
    # Основные действия
    buttons.append([
        InlineKeyboardButton(text="💬 Написать продавцу", callback_data=f"chat_{ad_id}"),
        InlineKeyboardButton(text="👤 Подписаться на продавца", callback_data=f"follow_seller_{ad_id}")
    ])
    
    # Жалоба и удаление
    row = [InlineKeyboardButton(text="⚠️ Пожаловаться", callback_data=f"complain_{ad_id}")]
    if can_delete:
        row.append(InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_ad_{ad_id}"))
    buttons.append(row)
    
    # Навигация
    if total_count > 1:
        nav_row = []
        if current_index > 0:
            nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_ad_{category}_{subcategory}_{current_index}"))
        nav_row.append(InlineKeyboardButton(text=f"{current_index + 1}/{total_count}", callback_data="current_page"))
        if current_index < total_count - 1:
            nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"next_ad_{category}_{subcategory}_{current_index}"))
        buttons.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_advertisement_actions_with_nav(ad_id, is_favorite=False, category="", subcategory="", current_index=0, total_count=1, can_delete=False):
    """Действия с объявлением с навигацией (алиас для совместимости)"""
    return get_advertisement_actions(ad_id, is_favorite, can_delete, category, subcategory, current_index, total_count)

def get_favorites_menu():
    """Меню избранного"""
    buttons = [
        [InlineKeyboardButton(text="📝 Избранные товары", callback_data="favorites_items")],
        [InlineKeyboardButton(text="👤 Избранные продавцы", callback_data="favorites_sellers")],
        [InlineKeyboardButton(text="📂 Избранные категории", callback_data="favorites_categories")],
        [InlineKeyboardButton(text="⚙️ Настройки уведомлений", callback_data="favorites_settings")],
        [InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_complaint_reasons_keyboard():
    """Клавиатура причин жалобы"""
    buttons = [
        [InlineKeyboardButton(text="🚫 Запрещенный товар", callback_data="complaint_reason_forbidden")],
        [InlineKeyboardButton(text="💰 Завышенная цена", callback_data="complaint_reason_overpriced")],
        [InlineKeyboardButton(text="📸 Некачественные фото", callback_data="complaint_reason_bad_photos")],
        [InlineKeyboardButton(text="📝 Ложное описание", callback_data="complaint_reason_fake_description")],
        [InlineKeyboardButton(text="👤 Мошенничество", callback_data="complaint_reason_scam")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_admin_panel():
    """Админ-панель"""
    buttons = [
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="⚠️ Жалобы", callback_data="admin_complaints")],
        [InlineKeyboardButton(text="🔗 Интеграции", callback_data="admin_integrations")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="🛡️ Верификация", callback_data="admin_verification")],
        [InlineKeyboardButton(text="🚫 Черный список", callback_data="admin_blacklist")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings")],
        [InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_admin_complaints_keyboard():
    """Клавиатура управления жалобами"""
    buttons = [
        [InlineKeyboardButton(text="🆕 Новые жалобы", callback_data="admin_complaints_pending")],
        [InlineKeyboardButton(text="✅ Решенные", callback_data="admin_complaints_resolved")],
        [InlineKeyboardButton(text="❌ Отклоненные", callback_data="admin_complaints_rejected")],
        [InlineKeyboardButton(text="🔙 Назад в админ-панель", callback_data="back_to_admin")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_admin_integrations_keyboard():
    """Клавиатура управления интеграциями"""
    buttons = [
        [InlineKeyboardButton(text="➕ Добавить интеграцию", callback_data="admin_add_integration")],
        [InlineKeyboardButton(text="📋 Список интеграций", callback_data="admin_list_integrations")],
        [InlineKeyboardButton(text="🗑️ Удалить интеграцию", callback_data="admin_delete_integration")],
        [InlineKeyboardButton(text="📊 Статистика интеграций", callback_data="admin_integrations_stats")],
        [InlineKeyboardButton(text="🔙 Назад в админ-панель", callback_data="back_to_admin")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_integration_types_keyboard():
    """Клавиатура типов интеграций"""
    buttons = [
        [InlineKeyboardButton(text="💬 Telegram чат", callback_data="integration_type_chat")],
        [InlineKeyboardButton(text="🌐 Веб-сайт", callback_data="integration_type_website")],
        [InlineKeyboardButton(text="📢 Telegram канал", callback_data="integration_type_channel")],
        [InlineKeyboardButton(text="🤖 Другой бот", callback_data="integration_type_bot")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_integrations")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_admin_users_keyboard():
    """Клавиатура управления пользователями"""
    buttons = [
        [InlineKeyboardButton(text="📊 Статистика пользователей", callback_data="admin_users_stats")],
        [InlineKeyboardButton(text="🚫 Забаненные пользователи", callback_data="admin_users_banned")],
        [InlineKeyboardButton(text="👥 Все пользователи", callback_data="admin_users_list")],
        [InlineKeyboardButton(text="🔙 Назад в админ-панель", callback_data="back_to_admin")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_admin_broadcast_keyboard():
    """Клавиатура рассылки"""
    buttons = [
        [InlineKeyboardButton(text="📢 Отправить всем", callback_data="admin_broadcast_send")],
        [InlineKeyboardButton(text="📋 История рассылок", callback_data="admin_broadcast_history")],
        [InlineKeyboardButton(text="🔙 Назад в админ-панель", callback_data="back_to_admin")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_admin_settings_keyboard():
    """Клавиатура настроек"""
    buttons = [
        [InlineKeyboardButton(text="💰 Настройки цен", callback_data="admin_settings_prices")],
        [InlineKeyboardButton(text="📸 Лимиты фото", callback_data="admin_settings_photos")],
        [InlineKeyboardButton(text="🔒 Безопасность", callback_data="admin_settings_security")],
        [InlineKeyboardButton(text="🔙 Назад в админ-панель", callback_data="back_to_admin")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_rules_keyboard():
    """Клавиатура правил"""
    buttons = [
        [InlineKeyboardButton(text="📋 Общие правила", callback_data="rules_general")],
        [InlineKeyboardButton(text="💰 Правила торговли", callback_data="rules_trading")],
        [InlineKeyboardButton(text="🚫 Запрещенные товары", callback_data="rules_forbidden")],
        [InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_chat_keyboard(ad_id):
    """Клавиатура чата"""
    buttons = [
        [InlineKeyboardButton(text="🔙 Назад к объявлению", callback_data=f"back_to_ad_{ad_id}")],
        [InlineKeyboardButton(text="📋 История чата", callback_data=f"chat_history_{ad_id}")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_pagination_keyboard(current_page, total_pages, callback_prefix):
    """Клавиатура пагинации"""
    buttons = []
    
    if total_pages > 1:
        row = []
        if current_page > 0:
            row.append(InlineKeyboardButton(text="⬅️", callback_data=f"{callback_prefix}_page_{current_page - 1}"))
        
        row.append(InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="current_page"))
        
        if current_page < total_pages - 1:
            row.append(InlineKeyboardButton(text="➡️", callback_data=f"{callback_prefix}_page_{current_page + 1}"))
        
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад к категориям", callback_data="back_to_categories")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard