from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SERVERS, COMPLAINT_REASONS

def get_servers_keyboard():
    """Клавиатура выбора сервера"""
    buttons = []
    # Разбиваем серверы на группы по 3
    for i in range(0, len(SERVERS), 3):
        row = []
        for j in range(3):
            if i + j < len(SERVERS):
                row.append(InlineKeyboardButton(text=SERVERS[i + j], callback_data=f"server_{SERVERS[i + j]}"))
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_search_filters_keyboard():
    """Клавиатура фильтров поиска"""
    buttons = [
        [InlineKeyboardButton(text="🔍 Поиск по названию", callback_data="search_by_title")],
        [InlineKeyboardButton(text="💰 Фильтр по цене", callback_data="filter_by_price")],
        [InlineKeyboardButton(text="🖥️ Фильтр по серверу", callback_data="filter_by_server")],
        [InlineKeyboardButton(text="⭐ Фильтр по рейтингу", callback_data="filter_by_rating")],
        [InlineKeyboardButton(text="📊 Сортировка", callback_data="sort_options")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_sort_options_keyboard():
    """Клавиатура опций сортировки"""
    buttons = [
        [InlineKeyboardButton(text="💰 По цене (возрастание)", callback_data="sort_price_asc")],
        [InlineKeyboardButton(text="💰 По цене (убывание)", callback_data="sort_price_desc")],
        [InlineKeyboardButton(text="📅 По дате (новые)", callback_data="sort_date_desc")],
        [InlineKeyboardButton(text="📅 По дате (старые)", callback_data="sort_date_asc")],
        [InlineKeyboardButton(text="⭐ По рейтингу", callback_data="sort_rating")],
        [InlineKeyboardButton(text="👁️ По просмотрам", callback_data="sort_views")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_search")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_verification_keyboard(ad_id):
    """Клавиатура верификации товара"""
    buttons = [
        [InlineKeyboardButton(text="✅ Одобрить", callback_data=f"verify_approve_{ad_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"verify_reject_{ad_id}")],
        [InlineKeyboardButton(text="📝 Добавить комментарий", callback_data=f"verify_comment_{ad_id}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_verification")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_guarantor_keyboard(ad_id):
    """Клавиатура системы гарантов"""
    buttons = [
        [InlineKeyboardButton(text="🛡️ Запросить гаранта", callback_data=f"request_guarantor_{ad_id}")],
        [InlineKeyboardButton(text="👤 Стать гарантом", callback_data=f"become_guarantor_{ad_id}")],
        [InlineKeyboardButton(text="📋 Список гарантов", callback_data="guarantors_list")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_ad")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_notification_settings_keyboard():
    """Клавиатура настроек уведомлений"""
    buttons = [
        [InlineKeyboardButton(text="🔔 Новые товары", callback_data="notify_new_items")],
        [InlineKeyboardButton(text="💬 Сообщения", callback_data="notify_messages")],
        [InlineKeyboardButton(text="💰 Скидки", callback_data="notify_discounts")],
        [InlineKeyboardButton(text="⭐ Избранные продавцы", callback_data="notify_favorite_sellers")],
        [InlineKeyboardButton(text="📂 Избранные категории", callback_data="notify_favorite_categories")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_analytics_keyboard():
    """Клавиатура аналитики"""
    buttons = [
        [InlineKeyboardButton(text="📈 Статистика продаж", callback_data="analytics_sales")],
        [InlineKeyboardButton(text="💰 Анализ цен", callback_data="analytics_prices")],
        [InlineKeyboardButton(text="👥 Популярные продавцы", callback_data="analytics_sellers")],
        [InlineKeyboardButton(text="📊 Тренды", callback_data="analytics_trends")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_blacklist_keyboard():
    """Клавиатура черного списка"""
    buttons = [
        [InlineKeyboardButton(text="🚫 Заблокировать пользователя", callback_data="blacklist_add")],
        [InlineKeyboardButton(text="📋 Список заблокированных", callback_data="blacklist_view")],
        [InlineKeyboardButton(text="✅ Разблокировать", callback_data="blacklist_remove")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

