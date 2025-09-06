from aiogram.fsm.state import State, StatesGroup

class AdvertisementStates(StatesGroup):
    """Состояния для создания объявления"""
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_category = State()
    waiting_for_subcategory = State()
    waiting_for_currency = State()
    waiting_for_price = State()
    waiting_for_condition = State()
    waiting_for_server = State()
    waiting_for_photos = State()

class ComplaintStates(StatesGroup):
    """Состояния для подачи жалобы"""
    waiting_for_reason = State()
    waiting_for_description = State()
    waiting_for_evidence = State()

class AdminStates(StatesGroup):
    """Состояния для админ-панели"""
    waiting_for_broadcast_message = State()
    waiting_for_integration_name = State()
    waiting_for_integration_url = State()
    waiting_for_integration_description = State()

class ChatStates(StatesGroup):
    """Состояния для чата между покупателем и продавцом"""
    waiting_for_message = State()

class SearchStates(StatesGroup):
    """Состояния для расширенного поиска"""
    waiting_for_search_query = State()
    waiting_for_price_min = State()
    waiting_for_price_max = State()
    waiting_for_server_filter = State()

class NotificationStates(StatesGroup):
    """Состояния для уведомлений"""
    waiting_for_notification_text = State()
    waiting_for_notification_target = State()

class VerificationStates(StatesGroup):
    """Состояния для верификации товаров"""
    waiting_for_verification_decision = State()
    waiting_for_verification_comment = State()

class GuarantorStates(StatesGroup):
    """Состояния для системы гарантов"""
    waiting_for_guarantor_request = State()
    waiting_for_guarantor_approval = State()