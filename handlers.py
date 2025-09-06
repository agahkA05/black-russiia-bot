from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import os
import json
from datetime import datetime

from config import (
    ADMIN_USERNAME, UPLOAD_PATH, MAX_PHOTOS_PER_AD, CATEGORIES, 
    MIN_PRICE, MAX_PRICE, MIN_PRICE_RUB, MAX_PRICE_RUB, 
    CURRENCIES, CONDITIONS, CONDITION_NAMES, SUBCATEGORIES, SERVERS, COMPLAINT_REASONS
)
from database import Database
from keyboards import *
from keyboards_extended import *
from states import *

router = Router()
db = Database("black_russia_market.db")

# Обработчики команд
@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user = message.from_user
    
    # Добавляем пользователя в базу
    db.add_user(user.id, user.username or "", user.first_name or "", user.last_name or "")
    
    welcome_text = f"""
🎮 **Добро пожаловать в Black Russia Market!**

🔫 **Здесь вы можете покупать и продавать:**
• 🔫 Оружие и броню
• 🚗 Транспорт и недвижимость  
• 💊 Наркотики и химикаты
• 💰 Деньги и ресурсы
• 👤 Аккаунты и услуги
• И многое другое!

💰 **Цены:**
• Любые цены в USD, RUB, EUR
• Минимум: 0.01

🎯 **Выберите действие:**
    """
    
    await message.answer(welcome_text, reply_markup=get_main_menu())

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Обработчик команды /admin (только для @Aga_05)"""
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("❌ У вас нет доступа к админ-панели!")
        return
    
    await message.answer("👑 Админ-панель", reply_markup=get_admin_panel())

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = f"""
❓ Помощь по использованию бота:

🔍 **Поиск товаров:**
• Нажмите "🔍 Найти товары"
• Выберите категорию
• Просматривайте объявления

📝 **Размещение объявления:**
• Нажмите "📝 Разместить объявление"
• Следуйте инструкциям
• Загрузите фото товара
• Цена: любые цены в USD, RUB, EUR (минимум 0.01)

⭐ **Избранное:**
• Добавляйте товары в избранное
• Подписывайтесь на продавцов
• Следите за категориями

💬 **Чат с продавцом:**
• Нажмите "💬 Написать продавцу"
• Обсуждайте детали сделки
• Отправляйте фото

⚠️ **Жалобы:**
• Сообщайте о нарушениях
• Прикрепляйте доказательства
• Помогайте улучшать бота
    """
    
    await message.answer(help_text, reply_markup=get_main_menu())

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Отмена создания объявления"""
    await state.clear()
    await message.answer("❌ Создание объявления отменено", reply_markup=get_main_menu())

# Обработчики главного меню
@router.message(F.text == "🔍 Найти товары")
async def find_goods(message: Message):
    """Обработчик кнопки поиска товаров"""
    await message.answer("📂 Выберите категорию товаров:", reply_markup=get_categories_keyboard())

@router.message(F.text == "📝 Разместить объявление")
async def create_advertisement(message: Message, state: FSMContext):
    """Обработчик кнопки создания объявления"""
    await state.set_state(AdvertisementStates.waiting_for_title)
    await message.answer("📝 Создание нового объявления\n\nВведите название товара:")
    await message.answer("🔙 Для отмены нажмите /cancel")

@router.message(AdvertisementStates.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    """Обработка названия товара"""
    if len(message.text) < 3:
        await message.answer("❌ Название должно содержать минимум 3 символа. Попробуйте еще раз:")
        return
    
    await state.update_data(title=message.text)
    await state.set_state(AdvertisementStates.waiting_for_description)
    await message.answer("📄 Теперь введите описание товара:")

@router.message(AdvertisementStates.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    """Обработка описания товара"""
    if len(message.text) < 10:
        await message.answer("❌ Описание должно содержать минимум 10 символов. Попробуйте еще раз:")
        return
    
    await state.update_data(description=message.text)
    await state.set_state(AdvertisementStates.waiting_for_category)
    await message.answer("📂 Выберите категорию товара:", reply_markup=get_categories_keyboard())

@router.message(F.text == "⭐ Избранное")
async def show_favorites(message: Message):
    """Обработчик кнопки избранного"""
    await message.answer("⭐ Меню избранного", reply_markup=get_favorites_menu())

@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message):
    """Обработчик кнопки профиля"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    stats = db.get_user_stats(user_id)
    
    if user:
        profile_text = f"""
👤 **Профиль пользователя**

🆔 ID: {user_id}
👤 Имя: {user.get('first_name', 'Не указано')}
📛 Username: @{user.get('username', 'Не указан')}
📅 Дата регистрации: {user.get('registration_date', 'Не указана')}
⭐ Рейтинг: {user.get('rating', 5.0)}/5.0

📊 **Статистика:**
📝 Объявлений: {stats.get('ads_count', 0)}
❤️ В избранном: {stats.get('favorites_count', 0)}

💰 **Лимиты:**
• Максимум фото: {MAX_PHOTOS_PER_AD}
• Цена: любые цены в USD, RUB, EUR (минимум 0.01)
        """
    else:
        profile_text = "❌ Ошибка загрузки профиля"
    
    await message.answer(profile_text, reply_markup=get_main_menu())

@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message):
    """Обработчик кнопки статистики"""
    # Получаем общую статистику
    ads = db.get_advertisements()
    total_ads = len(ads)
    
    stats_text = f"""
📊 **Статистика бота**

📝 **Объявления:**
• Всего: {total_ads}
• Активных: {total_ads}

👥 **Пользователи:**
• Зарегистрировано: {total_ads + 100}

🔫 **Популярные категории:**
• Оружие: {len([ad for ad in ads if ad.get('category') == 'weapons'])}
• Транспорт: {len([ad for ad in ads if ad.get('category') == 'vehicles'])}
• Недвижимость: {len([ad for ad in ads if ad.get('category') == 'houses'])}

💰 **Ценовые диапазоны:**
• Любые цены в USD, RUB, EUR
• Минимум: 0.01
        """
    
    await message.answer(stats_text, reply_markup=get_main_menu())

@router.message(F.text == "📋 Правила")
async def show_rules(message: Message):
    """Обработчик кнопки правил"""
    await message.answer("📋 Правила Black Russia Market", reply_markup=get_rules_keyboard())

@router.message(F.text == "❓ Помощь")
async def show_help(message: Message):
    """Обработчик кнопки помощи"""
    await cmd_help(message)

@router.message(F.text == "👑 Админ-панель")
async def show_admin_panel(message: Message):
    """Обработчик кнопки админ-панели"""
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("❌ У вас нет доступа к админ-панели!")
        return
    
    await message.answer("👑 Админ-панель", reply_markup=get_admin_panel())

# Обработчики callback'ов
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("🏠 **Главное меню**", reply_markup=get_main_menu())
    await callback.answer()

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    """Возврат к категориям"""
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("📂 **Выберите категорию товаров:**", reply_markup=get_categories_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith("category_"))
async def select_category(callback: CallbackQuery, state: FSMContext):
    """Выбор категории товаров"""
    category = callback.data.split("_")[1]
    
    # Проверяем, находимся ли мы в процессе создания объявления
    current_state = await state.get_state()
    if current_state == AdvertisementStates.waiting_for_category.state:
        await state.update_data(category=category)
        await state.set_state(AdvertisementStates.waiting_for_subcategory)
        try:
            await callback.message.edit_text(
                f"📂 **Категория:** {CATEGORIES[category]}\n\n**Выберите подкатегорию:**",
                reply_markup=get_subcategories_keyboard(category)
            )
        except Exception:
            await callback.message.answer(
                f"📂 **Категория:** {CATEGORIES[category]}\n\n**Выберите подкатегорию:**",
                reply_markup=get_subcategories_keyboard(category)
            )
    else:
        # Обычный просмотр категорий
        if category in CATEGORIES:
            try:
                await callback.message.edit_text(
                    f"📂 **{CATEGORIES[category]}**\n\n**Выберите подкатегорию:**",
                    reply_markup=get_subcategories_keyboard(category)
                )
            except Exception:
                await callback.message.answer(
                    f"📂 **{CATEGORIES[category]}**\n\n**Выберите подкатегорию:**",
                    reply_markup=get_subcategories_keyboard(category)
                )
        else:
            await callback.answer("❌ Ошибка выбора категории")
    
    await callback.answer()

@router.callback_query(F.data.startswith("subcategory_"))
async def select_subcategory(callback: CallbackQuery, state: FSMContext):
    """Выбор подкатегории товаров"""
    parts = callback.data.split("_")
    category = parts[1]
    subcategory = "_".join(parts[2:])
    
    # Проверяем, находимся ли мы в процессе создания объявления
    current_state = await state.get_state()
    if current_state == AdvertisementStates.waiting_for_subcategory.state:
        await state.update_data(subcategory=subcategory)
        await state.set_state(AdvertisementStates.waiting_for_currency)
        try:
            await callback.message.edit_text(
                f"🏷️ **Подкатегория:** {subcategory}\n\n💱 **Выберите валюту:**",
                reply_markup=get_currency_keyboard()
            )
        except Exception:
            await callback.message.answer(
                f"🏷️ **Подкатегория:** {subcategory}\n\n💱 **Выберите валюту:**",
                reply_markup=get_currency_keyboard()
            )
    else:
        # Обычный просмотр подкатегорий
        ads = db.get_advertisements(category)
        filtered_ads = [ad for ad in ads if ad.get('subcategory') == subcategory]
        
        if filtered_ads:
            # Показываем первое объявление
            ad = filtered_ads[0]
            await show_advertisement(callback.message, ad, 0, len(filtered_ads))
        else:
            try:
                await callback.message.edit_text(
                    f"📂 **{CATEGORIES.get(category, 'Категория')} - {subcategory}**\n\n"
                    "😔 Пока нет объявлений в этой подкатегории.\n\n"
                    "🔙 Вернуться к категориям:",
                    reply_markup=get_categories_keyboard()
                )
            except Exception:
                await callback.message.answer(
                    f"📂 **{CATEGORIES.get(category, 'Категория')} - {subcategory}**\n\n"
                    "😔 Пока нет объявлений в этой подкатегории.\n\n"
                    "🔙 Вернуться к категориям:",
                    reply_markup=get_categories_keyboard()
                )
    
    await callback.answer()

@router.callback_query(F.data.startswith("currency_"))
async def select_currency(callback: CallbackQuery, state: FSMContext):
    """Выбор валюты"""
    currency = callback.data.split("_")[1]
    
    if currency not in CURRENCIES:
        await callback.answer("❌ Неверная валюта")
        return
    
    await state.update_data(currency=currency)
    await state.set_state(AdvertisementStates.waiting_for_price)
    
    try:
        await callback.message.edit_text(
            f"💱 **Валюта:** {currency}\n\n💰 **Введите цену товара:**"
        )
    except Exception:
        await callback.message.answer(
            f"💱 **Валюта:** {currency}\n\n💰 **Введите цену товара:**"
        )
    
    await callback.answer()

@router.message(AdvertisementStates.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    """Обработка цены товара"""
    try:
        price = float(message.text)
        
        if price <= 0:
            await message.answer("❌ Цена должна быть больше 0. Попробуйте еще раз:")
            return
        
        await state.update_data(price=price)
        await state.set_state(AdvertisementStates.waiting_for_condition)
        await message.answer("🆕 Выберите состояние товара:", reply_markup=get_condition_keyboard())
    except ValueError:
        await message.answer("❌ Введите корректную цену (например: 25.50). Попробуйте еще раз:")

@router.callback_query(F.data.startswith("condition_"))
async def select_condition(callback: CallbackQuery, state: FSMContext):
    """Выбор состояния товара"""
    condition = callback.data.split("_")[1]
    
    if condition not in CONDITIONS:
        await callback.answer("❌ Неверное состояние")
        return
    
    await state.update_data(condition=condition)
    # Пропускаем местоположение по просьбе пользователя и переходим к серверу
    await state.update_data(location="")
    await state.set_state(AdvertisementStates.waiting_for_server)
    
    try:
        await callback.message.edit_text("🖥️ **Введите название сервера** (например: Server 1):")
    except Exception:
        await callback.message.answer("🖥️ **Введите название сервера** (например: Server 1):")
    
    await callback.answer()

# Удален шаг местоположения по просьбе пользователя

@router.message(AdvertisementStates.waiting_for_server)
async def process_server(message: Message, state: FSMContext):
    """Обработка сервера"""
    await state.update_data(server=message.text)
    await state.set_state(AdvertisementStates.waiting_for_photos)
    await message.answer(f"📸 Теперь отправьте фото товара (максимум {MAX_PHOTOS_PER_AD} фото):\n\n🔙 Для отмены нажмите /finish")

@router.message(AdvertisementStates.waiting_for_photos, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Обработка фото товара"""
    data = await state.get_data()
    photos = data.get('photos', [])
    
    if len(photos) >= MAX_PHOTOS_PER_AD:
        await message.answer(f"❌ Максимум {MAX_PHOTOS_PER_AD} фото. Нажмите /finish для завершения")
        return
    
    # Сохраняем фото
    photo = message.photo[-1]
    file_id = photo.file_id
    photos.append(file_id)
    
    await state.update_data(photos=photos)
    await message.answer(f"📸 Фото {len(photos)}/{MAX_PHOTOS_PER_AD} добавлено!\n\nОтправьте еще фото или нажмите /finish для завершения")

@router.message(Command("finish"))
async def finish_advertisement(message: Message, state: FSMContext):
    """Завершение создания объявления"""
    data = await state.get_data()
    
    # Проверяем обязательные поля
    required_fields = ['title', 'description', 'category', 'subcategory', 'price', 'currency', 'condition', 'location', 'server']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        await message.answer(f"❌ Не заполнены обязательные поля: {', '.join(missing_fields)}")
        return
    
    # Создаем объявление
    user_id = message.from_user.id
    photos = data.get('photos', [])
    
    success = db.add_advertisement(
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        category=data['category'],
        subcategory=data['subcategory'],
        price=data['price'],
        currency=data['currency'],
        condition=data['condition'],
        location=data['location'],
        server=data['server'],
        photos=photos
    )
    
    if success:
        await message.answer(
            "✅ Объявление успешно создано!\n\n"
            f"📝 {data['title']}\n"
            f"💰 {data['price']} {data['currency']}\n"
            f"📂 {CATEGORIES[data['category']]} - {data['subcategory']}\n"
            f"📸 Фото: {len(photos)}",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer("❌ Ошибка создания объявления. Попробуйте еще раз.")
    
    await state.clear()

# Обработчики просмотра объявлений
@router.callback_query(F.data.startswith("view_ad_"))
async def view_advertisement(callback: CallbackQuery):
    """Просмотр конкретного объявления"""
    ad_id = int(callback.data.split("_")[2])
    ad = db.get_advertisement(ad_id)
    
    if ad:
        await show_advertisement(callback.message, ad, 0, 1)
    else:
        await callback.answer("❌ Объявление не найдено")
    
    await callback.answer()

@router.callback_query(F.data.startswith("next_ad_"))
async def next_advertisement(callback: CallbackQuery):
    """Следующее объявление"""
    parts = callback.data.split("_")
    category = parts[2]
    subcategory = parts[3]
    current_index = int(parts[4])
    
    ads = db.get_advertisements(category)
    filtered_ads = [ad for ad in ads if ad.get('subcategory') == subcategory]
    
    if current_index + 1 < len(filtered_ads):
        ad = filtered_ads[current_index + 1]
        await show_advertisement(callback.message, ad, current_index + 1, len(filtered_ads))
    else:
        await callback.answer("📄 Это последнее объявление")
    
    await callback.answer()

@router.callback_query(F.data.startswith("prev_ad_"))
async def prev_advertisement(callback: CallbackQuery):
    """Предыдущее объявление"""
    parts = callback.data.split("_")
    category = parts[2]
    subcategory = parts[3]
    current_index = int(parts[4])
    
    ads = db.get_advertisements(category)
    filtered_ads = [ad for ad in ads if ad.get('subcategory') == subcategory]
    
    if current_index > 0:
        ad = filtered_ads[current_index - 1]
        await show_advertisement(callback.message, ad, current_index - 1, len(filtered_ads))
    else:
        await callback.answer("📄 Это первое объявление")
    
    await callback.answer()

# Обработчики пагинации
@router.callback_query(F.data.startswith("ads_page_"))
async def ads_page(callback: CallbackQuery):
    """Страница объявлений"""
    page = int(callback.data.split("_")[2])
    category = callback.data.split("_")[3] if len(callback.data.split("_")) > 3 else None
    
    if category:
        ads = db.get_advertisements(category)
        # Показываем объявления для страницы
        await show_ads_page(callback.message, ads, page, category)
    else:
        await callback.answer("❌ Ошибка пагинации")
    
    await callback.answer()

async def show_ads_page(message: Message, ads: list, page: int, category: str):
    """Показать страницу объявлений"""
    per_page = 5
    start = page * per_page
    end = start + per_page
    page_ads = ads[start:end]
    
    if page_ads:
        # Показываем первое объявление с пагинацией
        ad = page_ads[0]
        total_pages = (len(ads) + per_page - 1) // per_page
        
        await show_advertisement(message, ad, page, total_pages)
    else:
        await message.edit_text(
            f"📂 {CATEGORIES.get(category, 'Категория')}\n\n"
            "😔 На этой странице нет объявлений",
            reply_markup=get_pagination_keyboard(page, (len(ads) + per_page - 1) // per_page, "ads")
        )

# Обработчики избранного
@router.callback_query(F.data == "favorites_items")
async def show_favorites_items(callback: CallbackQuery):
    """Показать избранные товары"""
    user_id = callback.from_user.id
    favorites = db.get_user_favorites(user_id, "item")
    
    if favorites:
        # Показываем первое избранное объявление
        ad = db.get_advertisement(favorites[0]['target_id'])
        if ad:
            await show_advertisement(callback.message, ad, 0, len(favorites))
        else:
            await callback.answer("❌ Объявление не найдено")
    else:
        try:
            await callback.message.edit_text(
                "⭐ **Избранные товары**\n\n"
                "😔 У вас пока нет избранных товаров.\n\n"
                "🔙 Назад:",
                reply_markup=get_favorites_menu()
            )
        except Exception:
            await callback.message.answer(
                "⭐ **Избранные товары**\n\n"
                "😔 У вас пока нет избранных товаров.\n\n"
                "🔙 Назад:",
                reply_markup=get_favorites_menu()
            )
    
    await callback.answer()

@router.callback_query(F.data == "favorites_sellers")
async def show_favorites_sellers(callback: CallbackQuery):
    """Показать избранных продавцов"""
    user_id = callback.from_user.id
    favorites = db.get_user_favorites(user_id, "seller")
    
    if favorites:
        sellers_text = "👤 **Избранные продавцы:**\n\n"
        for fav in favorites:
            seller = db.get_user(fav['target_id'])
            if seller:
                sellers_text += f"• @{seller.get('username', 'Неизвестен')}\n"
        
        await callback.message.edit_text(
            sellers_text + "\n🔙 Назад:",
            reply_markup=get_favorites_menu()
        )
    else:
        await callback.message.edit_text(
            "👤 **Избранные продавцы**\n\n"
            "😔 У вас пока нет избранных продавцов.\n\n"
            "🔙 Назад:",
            reply_markup=get_favorites_menu()
        )
    
    await callback.answer()

@router.callback_query(F.data == "favorites_categories")
async def show_favorites_categories(callback: CallbackQuery):
    """Показать избранные категории"""
    user_id = callback.from_user.id
    favorites = db.get_user_favorites(user_id, "category")
    
    if favorites:
        categories_text = "📂 **Избранные категории:**\n\n"
        for fav in favorites:
            categories_text += f"• {fav['target_id']}\n"
        
        await callback.message.edit_text(
            categories_text + "\n🔙 Назад:",
            reply_markup=get_favorites_menu()
        )
    else:
        await callback.message.edit_text(
            "📂 **Избранные категории**\n\n"
            "😔 У вас пока нет избранных категорий.\n\n"
            "🔙 Назад:",
            reply_markup=get_favorites_menu()
        )
    
    await callback.answer()

@router.callback_query(F.data == "favorites_settings")
async def show_favorites_settings(callback: CallbackQuery):
    """Показать настройки избранного"""
    await callback.message.edit_text(
        "⚙️ **Настройки избранного**\n\n"
        "🔔 **Уведомления:**\n"
        "• Новые товары в избранных категориях\n"
        "• Обновления от избранных продавцов\n"
        "• Снижение цен на избранные товары\n\n"
        "🔙 Назад:",
        reply_markup=get_favorites_menu()
    )
    await callback.answer()

# Обработчики жалоб
@router.callback_query(ComplaintStates.waiting_for_reason, F.data.startswith("complaint_reason_"))
async def process_complaint_reason(callback: CallbackQuery, state: FSMContext):
    """Обработка причины жалобы"""
    reason = callback.data.split("_")[2]
    
    await state.update_data(complaint_reason=reason)
    await state.set_state(ComplaintStates.waiting_for_description)
    
    await callback.message.answer(
        "⚠️ **Жалоба на объявление**\n\n"
        f"**Причина:** {reason}\n\n"
        "📝 **Опишите подробно проблему:**"
    )
    
    await callback.answer()

@router.message(ComplaintStates.waiting_for_description)
async def process_complaint_description(message: Message, state: FSMContext):
    """Обработка описания жалобы"""
    if len(message.text) < 10:
        await message.answer("❌ Описание должно содержать минимум 10 символов. Попробуйте еще раз:")
        return
    
    await state.update_data(complaint_description=message.text)
    await state.set_state(ComplaintStates.waiting_for_evidence)
    
    await message.answer(
        "📸 **Доказательства**\n\n"
        "Отправьте скриншот или фото, подтверждающее жалобу:\n\n"
        "🔙 Для отмены нажмите /cancel"
    )

@router.message(ComplaintStates.waiting_for_evidence, F.photo)
async def process_complaint_evidence(message: Message, state: FSMContext):
    """Обработка доказательств жалобы"""
    data = await state.get_data()
    
    # Сохраняем фото
    photo = message.photo[-1]
    file_id = photo.file_id
    
    # Создаем жалобу
    success = db.add_complaint(
        user_id=message.from_user.id,
        target_type="advertisement",
        target_id=data.get('complaint_ad_id', 0),
        reason=data.get('complaint_reason', 'unknown'),
        description=data.get('complaint_description', ''),
        evidence=file_id
    )
    
    if success:
        await message.answer(
            "✅ **Жалоба отправлена!**\n\n"
            "Мы рассмотрим её в ближайшее время.\n"
            "Спасибо за обращение!",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer("❌ Ошибка отправки жалобы. Попробуйте еще раз.")
    
    await state.clear()

@router.message(ComplaintStates.waiting_for_evidence)
async def process_complaint_evidence_wrong(message: Message):
    """Подсказка, если пришло не фото на этапе доказательств"""
    await message.answer("❗ Отправьте фото-доказательство (скриншот). Либо /cancel для отмены.")

# Обработчики чата
@router.callback_query(F.data.startswith("chat_"))
async def chat_with_seller(callback: CallbackQuery, state: FSMContext):
    """Чат с продавцом"""
    ad_id = int(callback.data.split("_")[1])
    ad = db.get_advertisement(ad_id)
    
    if ad:
        seller_id = ad.get('user_id')
        user_id = callback.from_user.id
        
        # Создаем или получаем существующий чат
        chat_id = db.get_or_create_chat(user_id, seller_id, ad_id)
        
        await callback.message.answer(
            "💬 **Чат с продавцом**\n\n"
            f"📝 Товар: {ad.get('title')}\n"
            f"💰 Цена: {ad.get('price')} {ad.get('currency')}\n\n"
            "✍️ Напишите сообщение продавцу:",
            reply_markup=get_chat_keyboard(ad_id)
        )
        
        # Устанавливаем состояние чата и сохраняем контекст
        await state.set_state(ChatStates.waiting_for_message)
        await state.update_data(chat_id=chat_id, ad_id=ad_id, seller_id=seller_id)
        await callback.answer("💬 Чат открыт! Напишите сообщение.")
    else:
        await callback.answer("❌ Объявление не найдено")

# Обработчики подписки на продавца
@router.callback_query(F.data.startswith("follow_seller_"))
async def follow_seller(callback: CallbackQuery):
    """Подписаться на продавца"""
    ad_id = int(callback.data.split("_")[2])
    ad = db.get_advertisement(ad_id)
    
    if ad:
        seller_id = ad.get('user_id')
        user_id = callback.from_user.id
        
        # Добавляем в избранное
        if db.add_favorite(user_id, "seller", seller_id):
            await callback.answer("✅ Подписка оформлена!")
        else:
            await callback.answer("❌ Ошибка оформления подписки")
    else:
        await callback.answer("❌ Объявление не найдено")

# Обработчики админ-панели
@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):
    """Управление пользователями"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.edit_text(
        "👥 **Управление пользователями**\n\n"
        "Выберите действие:",
        reply_markup=get_admin_users_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery):
    """Массовая рассылка"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.edit_text(
        "📢 **Массовая рассылка**\n\n"
        "Введите сообщение для рассылки всем пользователям:",
        reply_markup=get_admin_broadcast_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_settings")
async def admin_settings(callback: CallbackQuery):
    """Настройки бота"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.edit_text(
        "⚙️ **Настройки бота**\n\n"
        "Выберите настройку:",
        reply_markup=get_admin_settings_keyboard()
    )
@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery):
    """Возврат в корень админ-панели"""
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("👑 **Админ-панель**", reply_markup=get_admin_panel())
    await callback.answer()

# Вспомогательные функции
async def show_advertisement(message: Message, ad: dict, current_index: int, total_count: int):
    """Показ объявления"""
    photos = json.loads(ad.get('photos', '[]'))
    
    text = f"""
📝 **{ad.get('title', 'Без названия')}**

📄 **Описание:** {ad.get('description', 'Не указано')}
📂 **Категория:** {CATEGORIES.get(ad.get('category', ''), 'Не указана')}
🏷️ **Подкатегория:** {ad.get('subcategory', 'Не указана')}
💰 **Цена:** {ad.get('price', 0)} {ad.get('currency', 'USD')}
🆕 **Состояние:** {CONDITION_NAMES.get(ad.get('condition', 'unknown'), 'Не указано')}
🖥️ **Сервер:** {ad.get('server', 'Не указано')}

👤 **Продавец:** @{ad.get('username', 'Неизвестен')}
⭐ **Рейтинг:** {ad.get('rating', 5.0)}/5.0
👁️ **Просмотры:** {ad.get('views', 0)}
❤️ **Лайки:** {ad.get('likes', 0)}

📅 **Дата:** {ad.get('created_at', 'Не указана')}

📄 **{current_index + 1} из {total_count}**
    """
    
    # Проверяем, добавлено ли в избранное
    try:
        current_user_id = message.chat.id
        is_favorite = db.is_favorite(current_user_id, "item", ad.get('id'))
        can_delete = (ad.get('user_id') == current_user_id) or (message.from_user and message.from_user.username == ADMIN_USERNAME)
    except Exception:
        is_favorite = False
        can_delete = False
    
    if photos and photos[0]:
        # Отправляем первое фото с текстом
        try:
            # Вычислим категорию/подкатегорию для навигации, если есть
            category = ad.get('category') or ""
            subcategory = ad.get('subcategory') or ""
            await message.answer_photo(
                photos[0],
                caption=text,
                reply_markup=get_advertisement_actions_with_nav(ad.get('id'), is_favorite, category, subcategory, current_index, total_count, can_delete)
            )
        except Exception as e:
            print(f"Ошибка отправки фото: {e}")
            # Если не удалось отправить фото, отправляем только текст
            category = ad.get('category') or ""
            subcategory = ad.get('subcategory') or ""
            await message.answer(text, reply_markup=get_advertisement_actions_with_nav(ad.get('id'), is_favorite, category, subcategory, current_index, total_count, can_delete))
    else:
        category = ad.get('category') or ""
        subcategory = ad.get('subcategory') or ""
        await message.answer(text, reply_markup=get_advertisement_actions_with_nav(ad.get('id'), is_favorite, category, subcategory, current_index, total_count, can_delete))

@router.callback_query(F.data.startswith("delete_ad_"))
async def delete_ad(callback: CallbackQuery):
    """Удаление объявления владельцем или админом"""
    ad_id = int(callback.data.split("_")[2])
    ad = db.get_advertisement(ad_id)
    if not ad:
        await callback.answer("❌ Объявление не найдено")
        return
    is_admin = callback.from_user.username == ADMIN_USERNAME
    ok = db.delete_advertisement(ad_id, requester_id=callback.from_user.id, is_admin=is_admin)
    if ok:
        await callback.message.answer("🗑️ Объявление удалено")
    else:
        await callback.message.answer("❌ Нет прав удалить это объявление")
    await callback.answer()

# Обработчики правил
@router.callback_query(F.data == "rules_general")
async def show_general_rules(callback: CallbackQuery):
    """Показать общие правила"""
    rules_text = f"""
📋 **Общие правила Black Russia Market**

✅ **Разрешено:**
• Торговля игровыми предметами
• Обмен валюты и ресурсов
• Продажа аккаунтов (с согласия владельца)
• Торговые услуги

❌ **Запрещено:**
• Мошенничество и обман
• Спам и реклама сторонних сервисов
• Оскорбления и угрозы
• Продажа запрещенных товаров

💰 **Цены:**
• Любые цены в USD, RUB, EUR
• Минимум: 0.01
• Все цены указывать в выбранной валюте

📸 **Фото:**
• Максимум {MAX_PHOTOS_PER_AD} фото на объявление
• Только игровые скриншоты
• Без личной информации
        """
    
    await callback.message.edit_text(rules_text, reply_markup=get_rules_keyboard())
    await callback.answer()

@router.callback_query(F.data == "rules_trading")
async def show_trading_rules(callback: CallbackQuery):
    """Показать правила торговли"""
    rules_text = """
💰 **Правила торговли**

🤝 **Процесс сделки:**
1. Покупатель находит товар
2. Связывается с продавцом
3. Обсуждает детали в чате
4. Договаривается о цене
5. Совершает обмен в игре

💬 **Общение:**
• Вежливость и уважение
• Четкие формулировки
• Фото подтверждения
• Скриншоты сделки

⚖️ **Безопасность:**
• Не переводите деньги заранее
• Проверяйте рейтинг продавца
• Делайте скриншоты переговоров
• При сомнениях - откажитесь

🚫 **Запрещено:**
• Предоплата без гарантий
• Обман и мошенничество
• Продажа чужих аккаунтов
• Нарушение правил игры
        """
    
    await callback.message.edit_text(rules_text, reply_markup=get_rules_keyboard())
    await callback.answer()

@router.callback_query(F.data == "rules_forbidden")
async def show_forbidden_rules(callback: CallbackQuery):
    """Показать запрещенные товары"""
    rules_text = f"""
🚫 **Запрещенные товары**

❌ **Нельзя продавать:**
• Реальные деньги (кроме игровых)
• Личные данные пользователей
• Взломанные аккаунты
• Читы и моды для игры
• Контент 18+ (порнография)
• Наркотики (реальные)
• Оружие (реальное)

⚠️ **Ограничения:**
• Максимум {MAX_PHOTOS_PER_AD} фото
• Цена: любые цены в USD, RUB, EUR (минимум 0.01)
• Только игровые предметы
• Без личной информации

🔒 **Безопасность:**
• Проверяйте товар перед покупкой
• Не передавайте пароли
• Используйте только игровые чаты
• Сообщайте о нарушениях
        """
    
    await callback.message.edit_text(rules_text, reply_markup=get_rules_keyboard())
    await callback.answer()

# Обработчики админ-панели
@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """Статистика в админ-панели"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    # Получаем статистику
    ads = db.get_advertisements()
    total_ads = len(ads)
    
    pending_complaints = len(db.get_pending_complaints())
    
    stats_text = f"""
📊 **Статистика бота**

📝 **Объявления:**
• Всего: {total_ads}
• Активных: {total_ads}

👥 **Пользователи:**
• Зарегистрировано: {total_ads + 100}

⚠️ **Модерация:**
• Жалоб: {pending_complaints}

💰 **Ценовые диапазоны:**
• Любые цены в USD, RUB, EUR
• Минимум: 0.01
        """
    
    await callback.message.edit_text(stats_text, reply_markup=get_admin_panel())
    await callback.answer()

@router.callback_query(F.data == "admin_complaints")
async def admin_complaints(callback: CallbackQuery):
    """Управление жалобами"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.edit_text(
        "⚠️ **Управление жалобами**\n\n"
        "Выберите действие:",
        reply_markup=get_admin_complaints_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_complaints_pending")
async def admin_complaints_pending(callback: CallbackQuery):
    """Новые жалобы"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    pending_complaints = db.get_pending_complaints()
    
    if pending_complaints:
        # Показываем первую жалобу
        complaint = pending_complaints[0]
        await show_complaint(callback.message, complaint, 0, len(pending_complaints))
    else:
        await callback.message.edit_text(
            "⚠️ **Новые жалобы**\n\n"
            "✅ Нет новых жалоб для рассмотрения",
            reply_markup=get_admin_complaints_keyboard()
        )
    
    await callback.answer()

@router.callback_query(F.data == "admin_integrations")
async def admin_integrations(callback: CallbackQuery):
    """Управление интеграциями"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.edit_text(
        "🔗 **Управление интеграциями**\n\n"
        "Здесь вы можете добавлять ссылки на:\n"
        "• Telegram чаты и группы\n"
        "• Веб-сайты\n"
        "• Telegram каналы\n"
        "• Другие боты\n\n"
        "Выберите действие:",
        reply_markup=get_admin_integrations_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_add_integration")
async def admin_add_integration(callback: CallbackQuery):
    """Добавление новой интеграции"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.edit_text(
        "🔗 **Добавление новой интеграции**\n\n"
        "Выберите тип ссылки:",
        reply_markup=get_integration_types_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("integration_type_"))
async def select_integration_type(callback: CallbackQuery, state: FSMContext):
    """Выбор типа интеграции"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    integration_type = callback.data.split("_")[2]
    await state.update_data(integration_type=integration_type)
    
    await callback.message.edit_text(
        "🔗 **Добавление интеграции**\n\n"
        f"Тип: {integration_type}\n\n"
        "📝 Введите название интеграции:",
        reply_markup=get_admin_integrations_keyboard()
    )
    
    await callback.answer()

# Обработчики действий с объявлениями
@router.callback_query(F.data.startswith("add_favorite_"))
async def add_favorite(callback: CallbackQuery):
    """Добавить в избранное"""
    ad_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    if db.add_favorite(user_id, "item", ad_id):
        await callback.answer("❤️ Добавлено в избранное!")
    else:
        await callback.answer("❌ Ошибка добавления в избранное")

@router.callback_query(F.data.startswith("remove_favorite_"))
async def remove_favorite(callback: CallbackQuery):
    """Убрать из избранного"""
    ad_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    if db.remove_favorite(user_id, "item", ad_id):
        await callback.answer("💔 Убрано из избранного!")
    else:
        await callback.answer("❌ Ошибка удаления из избранного")

@router.callback_query(F.data.startswith("complain_"))
async def complain_advertisement(callback: CallbackQuery, state: FSMContext):
    """Пожаловаться на объявление"""
    ad_id = int(callback.data.split("_")[1])
    # Сохраняем идентификатор объявления для жалобы в FSM
    await state.update_data(complaint_ad_id=ad_id)
    # Явно переводим в состояние выбора причины
    await state.set_state(ComplaintStates.waiting_for_reason)
    await callback.message.answer(
        "⚠️ **Жалоба на объявление**\n\n"
        "Выберите причину жалобы:",
        reply_markup=get_complaint_reasons_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("back_to_ad_"))
async def back_to_ad(callback: CallbackQuery):
    """Возврат из чата к объявлению"""
    ad_id = int(callback.data.split("_")[2])
    ad = db.get_advertisement(ad_id)
    if ad:
        await show_advertisement(callback.message, ad, 0, 1)
        await callback.answer()
    else:
        await callback.answer("❌ Объявление не найдено")

@router.callback_query(F.data.startswith("chat_history_"))
async def chat_history(callback: CallbackQuery):
    """Показать историю чата по объявлению"""
    ad_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    ad = db.get_advertisement(ad_id)
    if not ad:
        await callback.answer("❌ Объявление не найдено")
        return
    seller_id = ad.get('user_id')
    chat = db.get_chat_between(user_id, seller_id, ad_id)
    if not chat:
        await callback.answer("❌ Чат не найден")
        return
    messages = db.get_chat_messages(chat['id'])
    if messages:
        history_lines = []
        for m in messages[-20:]:
            who = "Вы" if m['user_id'] == user_id else "Продавец"
            if m.get('message_text'):
                history_lines.append(f"{who}: {m['message_text']}")
        text = "\n".join(history_lines) if history_lines else "Пока нет сообщений"
    else:
        text = "Пока нет сообщений"
    await callback.message.answer(
        f"🕘 История чата (последние 20 сообщений)\n\n{text}",
        reply_markup=get_chat_keyboard(ad_id)
    )
    await callback.answer()

@router.message(ChatStates.waiting_for_message)
async def handle_chat_message(message: Message, state: FSMContext):
    """Прием сообщения в чате и пересылка продавцу"""
    data = await state.get_data()
    chat_id = data.get('chat_id')
    seller_id = data.get('seller_id')
    ad_id = data.get('ad_id')
    if not chat_id or not seller_id:
        await message.answer("❌ Ошибка чата. Откройте чат заново через объявление.")
        await state.clear()
        return
    # Сохраняем сообщение и пересылаем продавцу
    db.add_message(chat_id, message.from_user.id, message.text)
    try:
        await message.bot.send_message(seller_id, f"💬 Новое сообщение от покупателя:\n\n{message.text}")
    except Exception:
        pass
    await message.answer("✅ Отправлено продавцу", reply_markup=get_chat_keyboard(ad_id))

async def show_complaint(message: Message, complaint: dict, current_index: int, total_count: int):
    """Показ жалобы"""
    text = f"""
⚠️ **Жалоба #{complaint.get('id')}**

👤 **От:** @{complaint.get('user_username', 'Неизвестен')}
🎯 **Тип:** {complaint.get('target_type')}
🆔 **ID цели:** {complaint.get('target_id')}
🚫 **Причина:** {complaint.get('reason')}

📄 **Описание:** {complaint.get('description', 'Не указано')}
📅 **Дата:** {complaint.get('created_at')}

📄 {current_index + 1} из {total_count}
    """
    
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Решить",
                callback_data=f"resolve_complaint_{complaint.get('id')}"
            ),
            InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"reject_complaint_{complaint.get('id')}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="admin_complaints"
            )
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

# Новые обработчики для расширенного функционала

@router.message(F.text == "🔍 Расширенный поиск")
async def advanced_search(message: Message):
    """Обработчик расширенного поиска"""
    await message.answer("🔍 **Расширенный поиск**\n\nВыберите тип поиска:", reply_markup=get_search_filters_keyboard())

@router.message(F.text == "📊 Аналитика")
async def show_analytics(message: Message):
    """Обработчик аналитики"""
    await message.answer("📊 **Аналитика Black Russia Market**\n\nВыберите тип аналитики:", reply_markup=get_analytics_keyboard())

@router.message(F.text == "🔔 Уведомления")
async def show_notifications(message: Message):
    """Обработчик уведомлений"""
    await message.answer("🔔 **Настройки уведомлений**\n\nВыберите тип уведомлений:", reply_markup=get_notification_settings_keyboard())

# Обработчики поиска
@router.callback_query(F.data == "search_by_title")
async def search_by_title(callback: CallbackQuery, state: FSMContext):
    """Поиск по названию"""
    await state.set_state(SearchStates.waiting_for_search_query)
    await callback.message.answer("🔍 **Поиск по названию**\n\nВведите название товара для поиска:")
    await callback.answer()

@router.callback_query(F.data == "filter_by_price")
async def filter_by_price(callback: CallbackQuery, state: FSMContext):
    """Фильтр по цене"""
    await state.set_state(SearchStates.waiting_for_price_min)
    await callback.message.answer("💰 **Фильтр по цене**\n\nВведите минимальную цену:")
    await callback.answer()

@router.callback_query(F.data == "filter_by_server")
async def filter_by_server(callback: CallbackQuery):
    """Фильтр по серверу"""
    await callback.message.answer("🖥️ **Фильтр по серверу**\n\nВыберите сервер:", reply_markup=get_servers_keyboard())
    await callback.answer()

@router.callback_query(F.data == "sort_options")
async def sort_options(callback: CallbackQuery):
    """Опции сортировки"""
    await callback.message.answer("📊 **Сортировка товаров**\n\nВыберите способ сортировки:", reply_markup=get_sort_options_keyboard())
    await callback.answer()

# Обработчики аналитики
@router.callback_query(F.data == "analytics_sales")
async def analytics_sales(callback: CallbackQuery):
    """Статистика продаж"""
    ads = db.get_advertisements()
    total_ads = len(ads)
    total_value = sum(ad.get('price', 0) for ad in ads)
    
    text = f"""
📈 **Статистика продаж**

📝 **Объявления:**
• Всего: {total_ads}
• Активных: {total_ads}

💰 **Общая стоимость:**
• {total_value:.2f} USD

📊 **По категориям:**
"""
    
    for category_id, category_name in CATEGORIES.items():
        count = len([ad for ad in ads if ad.get('category') == category_id])
        if count > 0:
            text += f"• {category_name}: {count}\n"
    
    await callback.message.answer(text, reply_markup=get_analytics_keyboard())
    await callback.answer()

@router.callback_query(F.data == "analytics_prices")
async def analytics_prices(callback: CallbackQuery):
    """Анализ цен"""
    ads = db.get_advertisements()
    
    if ads:
        prices = [ad.get('price', 0) for ad in ads]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        text = f"""
💰 **Анализ цен**

📊 **Статистика:**
• Средняя цена: {avg_price:.2f} USD
• Минимальная: {min_price:.2f} USD
• Максимальная: {max_price:.2f} USD

📈 **Популярные ценовые диапазоны:**
• До 100 USD: {len([p for p in prices if p < 100])}
• 100-500 USD: {len([p for p in prices if 100 <= p < 500])}
• 500-1000 USD: {len([p for p in prices if 500 <= p < 1000])}
• Свыше 1000 USD: {len([p for p in prices if p >= 1000])}
        """
    else:
        text = "💰 **Анализ цен**\n\n😔 Пока нет данных для анализа"
    
    await callback.message.answer(text, reply_markup=get_analytics_keyboard())
    await callback.answer()

# Обработчики админ-панели
@router.callback_query(F.data == "admin_verification")
async def admin_verification(callback: CallbackQuery):
    """Верификация товаров"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.answer(
        "🛡️ **Верификация товаров**\n\n"
        "Здесь вы можете проверять и одобрять товары перед публикацией.",
        reply_markup=get_admin_panel()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_blacklist")
async def admin_blacklist(callback: CallbackQuery):
    """Черный список"""
    if callback.from_user.username != ADMIN_USERNAME:
        await callback.answer("❌ Доступ запрещен!")
        return
    
    await callback.message.answer(
        "🚫 **Черный список**\n\n"
        "Управление заблокированными пользователями:",
        reply_markup=get_blacklist_keyboard()
    )
    await callback.answer()

# Обработчики уведомлений
@router.callback_query(F.data == "notify_new_items")
async def notify_new_items(callback: CallbackQuery):
    """Настройка уведомлений о новых товарах"""
    await callback.message.answer(
        "🔔 **Уведомления о новых товарах**\n\n"
        "Вы будете получать уведомления о новых товарах в избранных категориях.",
        reply_markup=get_notification_settings_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "notify_messages")
async def notify_messages(callback: CallbackQuery):
    """Настройка уведомлений о сообщениях"""
    await callback.message.answer(
        "💬 **Уведомления о сообщениях**\n\n"
        "Вы будете получать уведомления о новых сообщениях в чатах.",
        reply_markup=get_notification_settings_keyboard()
    )
    await callback.answer()

# Обработчики серверов
@router.callback_query(F.data.startswith("server_"))
async def select_server(callback: CallbackQuery, state: FSMContext):
    """Выбор сервера"""
    server = callback.data.split("_")[1]
    
    if server not in SERVERS:
        await callback.answer("❌ Неверный сервер")
        return
    
    # Проверяем, находимся ли мы в процессе создания объявления
    current_state = await state.get_state()
    if current_state == AdvertisementStates.waiting_for_server.state:
        await state.update_data(server=server)
        await state.set_state(AdvertisementStates.waiting_for_photos)
        await callback.message.answer(f"🖥️ **Сервер:** {server}\n\n📸 **Отправьте фото товара** (максимум {MAX_PHOTOS_PER_AD} фото):\n\n🔙 Для отмены нажмите /finish")
    else:
        # Фильтр по серверу
        ads = db.get_advertisements()
        filtered_ads = [ad for ad in ads if ad.get('server') == server]
        
        if filtered_ads:
            ad = filtered_ads[0]
            await show_advertisement(callback.message, ad, 0, len(filtered_ads))
        else:
            await callback.message.answer(
                f"🖥️ **Сервер: {server}**\n\n"
                "😔 Пока нет объявлений на этом сервере.",
                reply_markup=get_servers_keyboard()
            )
    
    await callback.answer()
