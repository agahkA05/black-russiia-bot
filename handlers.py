from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
import json

from config import (
    ADMIN_USERNAME, CATEGORIES, SUBCATEGORIES, CURRENCIES, 
    CONDITIONS, CONDITION_NAMES, SERVERS, COMPLAINT_REASONS
)
from database import Database

router = Router()
db = Database("black_russia_market.db")

# FSM состояния
class AdvertisementStates(StatesGroup):
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
    waiting_for_reason = State()
    waiting_for_description = State()
    waiting_for_evidence = State()

# Клавиатуры
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

# Обработчики команд
@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Добавляем пользователя в базу
    db.add_user(user_id, username, first_name, last_name)
    
    await message.answer(
        "🎮 **Добро пожаловать в Black Russia Bot!**\n\n"
        "Здесь ты можешь покупать и продавать игровые предметы!\n\n"
        "**Выбери действие:**",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    """Отмена текущего действия"""
    await state.clear()
    await message.answer("❌ Действие отменено!", reply_markup=get_main_menu())

# Обработчики кнопок
@router.message(F.text == "🔍 Найти товары")
async def search_items(message: Message):
    """Поиск товаров"""
    ads = db.get_advertisements(limit=10)
    
    if not ads:
        await message.answer("📭 Пока нет объявлений. Будь первым!")
        return
    
    text = "🔍 **Найденные товары:**\n\n"
    for i, ad in enumerate(ads, 1):
        text += f"**{i}.** 📦 **{ad[2]}**\n"
        text += f"💰 Цена: {ad[6]} {ad[7]}\n"
        text += f"🏷️ Категория: {ad[3]}\n"
        text += f"👤 Продавец: @{ad[9] or 'Не указан'}\n"
        text += f"🕒 {ad[10]}\n\n"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "📝 Разместить объявление")
async def create_ad(message: Message, state: FSMContext):
    """Создание объявления"""
    await state.set_state(AdvertisementStates.waiting_for_title)
    await message.answer(
        "📝 **Создание объявления**\n\n"
        "Введи название товара:",
        parse_mode="Markdown"
    )

@router.message(AdvertisementStates.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    """Обработка названия"""
    await state.update_data(title=message.text)
    await state.set_state(AdvertisementStates.waiting_for_description)
    await message.answer(
        "📝 **Описание товара**\n\n"
        "Опиши товар подробно:",
        parse_mode="Markdown"
    )

@router.message(AdvertisementStates.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    """Обработка описания"""
    await state.update_data(description=message.text)
    await state.set_state(AdvertisementStates.waiting_for_category)
    await message.answer(
        "🏷️ **Выбери категорию:**",
        reply_markup=get_categories_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    """Обработка категории"""
    category = callback.data.split("_")[1]
    await state.update_data(category=category)
    await state.set_state(AdvertisementStates.waiting_for_subcategory)
    
    await callback.message.edit_text(
        f"🏷️ **Выбери подкатегорию:**",
        reply_markup=get_subcategories_keyboard(category),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("sub_"))
async def process_subcategory(callback: CallbackQuery, state: FSMContext):
    """Обработка подкатегории"""
    subcategory = callback.data.split("_")[1]
    await state.update_data(subcategory=subcategory)
    await state.set_state(AdvertisementStates.waiting_for_currency)
    
    await callback.message.edit_text(
        "💱 **Выбери валюту:**",
        reply_markup=get_currencies_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("curr_"))
async def process_currency(callback: CallbackQuery, state: FSMContext):
    """Обработка валюты"""
    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)
    await state.set_state(AdvertisementStates.waiting_for_price)
    
    await callback.message.edit_text(
        f"💰 **Введи цену в {currency}:**\n\n"
        "Например: 1000",
        parse_mode="Markdown"
    )

@router.message(AdvertisementStates.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    """Обработка цены"""
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await state.set_state(AdvertisementStates.waiting_for_condition)
        
        await message.answer(
            "🔧 **Выбери состояние товара:**",
            reply_markup=get_conditions_keyboard(),
            parse_mode="Markdown"
        )
    except ValueError:
        await message.answer("❌ Введи корректную цену (число)!")

@router.callback_query(F.data.startswith("cond_"))
async def process_condition(callback: CallbackQuery, state: FSMContext):
    """Обработка состояния"""
    condition = callback.data.split("_")[1]
    await state.update_data(condition=condition)
    await state.set_state(AdvertisementStates.waiting_for_server)
    
    await callback.message.edit_text(
        "🌐 **Выбери сервер:**",
        reply_markup=get_servers_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("serv_"))
async def process_server(callback: CallbackQuery, state: FSMContext):
    """Обработка сервера"""
    server = callback.data.split("_")[1]
    await state.update_data(server=server)
    await state.set_state(AdvertisementStates.waiting_for_photos)
    
    await callback.message.edit_text(
        "📸 **Прикрепи фото товара:**\n\n"
        "Можешь отправить несколько фото подряд.\n"
        "Когда закончишь, отправь /done",
        parse_mode="Markdown"
    )

@router.message(AdvertisementStates.waiting_for_photos)
async def process_photos(message: Message, state: FSMContext):
    """Обработка фото"""
    if message.photo:
        # Сохраняем file_id фото
        photo_id = message.photo[-1].file_id
        data = await state.get_data()
        photos = data.get('photos', [])
        photos.append(photo_id)
        await state.update_data(photos=photos)
        
        await message.answer(f"📸 Фото добавлено! ({len(photos)}/10)\n\nОтправь еще фото или /done для завершения")
    else:
        await message.answer("❌ Отправь фото товара!")

@router.message(Command("done"))
async def finish_advertisement(message: Message, state: FSMContext):
    """Завершение создания объявления"""
    data = await state.get_data()
    
    if not data.get('title'):
        await message.answer("❌ Сначала создай объявление!")
        return
    
    # Сохраняем объявление
    photos_str = json.dumps(data.get('photos', []))
    db.add_advertisement(
        user_id=message.from_user.id,
        title=data['title'],
        description=data['description'],
        category=data['category'],
        subcategory=data['subcategory'],
        price=data['price'],
        currency=data['currency'],
        condition=data['condition'],
        server=data['server'],
        photos=photos_str
    )
    
    await state.clear()
    await message.answer(
        "✅ **Объявление создано!**\n\n"
        f"📦 Название: {data['title']}\n"
        f"💰 Цена: {data['price']} {data['currency']}\n"
        f"🏷️ Категория: {CATEGORIES[data['category']]}\n"
        f"🌐 Сервер: {data['server']}\n\n"
        "Твое объявление появится в поиске!",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.message(F.text == "⭐ Избранное")
async def favorites(message: Message):
    """Избранное"""
    await message.answer("⭐ **Избранное**\n\nПока пусто. Добавь товары в избранное!")

@router.message(F.text == "👤 Профиль")
async def profile(message: Message):
    """Профиль пользователя"""
    user_id = message.from_user.id
    ads = db.get_advertisements()
    user_ads = [ad for ad in ads if ad[1] == user_id]
    
    text = f"👤 **Твой профиль**\n\n"
    text += f"🆔 ID: {user_id}\n"
    text += f"📝 Объявлений: {len(user_ads)}\n"
    text += f"⭐ Рейтинг: 5.0\n"
    text += f"💰 Продаж: 0\n"
    text += f"🛒 Покупок: 0\n"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "🔍 Расширенный поиск")
async def advanced_search(message: Message):
    """Расширенный поиск"""
    await message.answer("🔍 **Расширенный поиск**\n\nПока в разработке!")

@router.message(F.text == "📊 Аналитика")
async def analytics(message: Message):
    """Аналитика"""
    await message.answer("📊 **Аналитика**\n\nПока в разработке!")

@router.message(F.text == "🔔 Уведомления")
async def notifications(message: Message):
    """Уведомления"""
    await message.answer("🔔 **Уведомления**\n\nПока в разработке!")

@router.message(F.text == "📋 Правила")
async def rules(message: Message):
    """Правила"""
    text = "📋 **Правила Black Russia Bot**\n\n"
    text += "1. 🚫 Запрещены мошенничество и обман\n"
    text += "2. 📸 Обязательно прикрепляй фото товара\n"
    text += "3. 💰 Указывай реальную цену\n"
    text += "4. 🏷️ Правильно выбирай категорию\n"
    text += "5. 👤 Не создавай фейковые аккаунты\n"
    text += "6. 🌐 Указывай правильный сервер\n"
    text += "7. 📝 Подробно описывай товар\n\n"
    text += "**Нарушение правил = бан! ⚠️**"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "❓ Помощь")
async def help_command(message: Message):
    """Помощь"""
    text = "❓ **Помощь**\n\n"
    text += "🔍 **Найти товары** - просмотр объявлений\n"
    text += "📝 **Разместить объявление** - создать новое\n"
    text += "⭐ **Избранное** - сохраненные товары\n"
    text += "👤 **Профиль** - твоя статистика\n"
    text += "🔍 **Расширенный поиск** - фильтры и сортировка\n"
    text += "📊 **Аналитика** - статистика продаж\n"
    text += "🔔 **Уведомления** - настройки уведомлений\n"
    text += "📋 **Правила** - правила использования\n\n"
    text += "**По вопросам: @Aga_05**"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "👑 Админ-панель")
async def admin_panel(message: Message):
    """Админ-панель"""
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("❌ У тебя нет прав доступа!")
        return
    
    text = "👑 **Админ-панель**\n\n"
    text += "🔧 **Управление пользователями**\n"
    text += "📊 **Статистика**\n"
    text += "📢 **Рассылки**\n"
    text += "⚙️ **Настройки**\n"
    text += "🛡️ **Модерация**\n\n"
    text += "Пока в разработке!"
    
    await message.answer(text, parse_mode="Markdown")

# Обработчики отмены
@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    """Отмена действия"""
    await state.clear()
    await callback.message.edit_text("❌ Действие отменено!")
    await callback.message.answer("Выбери действие:", reply_markup=get_main_menu())

@router.callback_query(F.data == "cancel_complaint")
async def cancel_complaint(callback: CallbackQuery, state: FSMContext):
    """Отмена жалобы"""
    await state.clear()
    await callback.message.edit_text("❌ Жалоба отменена!")

# Обработчик всех остальных сообщений
@router.message()
async def echo(message: Message):
    """Обработчик всех остальных сообщений"""
    await message.answer("Не понимаю. Используй кнопки меню! 🤔")