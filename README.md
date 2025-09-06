# 🎮 Black Russia Bot - Маркетплейс для игры

Telegram бот для покупки и продажи игровых предметов в Black Russia.

## 🚀 Деплой на Render

### Быстрый деплой:
1. Зайди на [render.com](https://render.com)
2. Создай новый Web Service
3. Подключи этот GitHub репозиторий
4. Добавь переменную окружения:
   ```
   BOT_TOKEN = 8172843951:AAFHMnhFITsIlnA9EwgpVenTHg47UO64bys
   ```
5. Нажми Deploy!

## ✨ Функции:
- 🔍 Поиск товаров
- 📝 Размещение объявлений
- ⭐ Система избранного
- 👤 Профиль пользователя
- 📊 Аналитика
- 🔔 Уведомления
- 📋 Правила
- 👑 Админ-панель

## 🛠️ Технологии:
- Python 3.10
- aiogram 3.0
- SQLite
- aiohttp

## 📁 Структура проекта:
```
├── main.py              # Главный файл
├── config.py            # Конфигурация
├── database.py          # База данных
├── handlers.py          # Обработчики
├── keyboards.py         # Клавиатуры
├── states.py            # FSM состояния
├── requirements.txt     # Зависимости
└── render.yaml         # Конфиг для Render
```

## 🎯 Готов к деплою!
Просто подключи к Render и добавь BOT_TOKEN! 🚀