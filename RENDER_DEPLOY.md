# 🚀 Деплой бота на Render

## 📋 Пошаговая инструкция:

### 1. **Создаем аккаунт на Render**
- Переходим на [render.com](https://render.com)
- Нажимаем "Get Started for Free"
- Регистрируемся через GitHub

### 2. **Создаем новый Web Service**
- Нажимаем "New +" → "Web Service"
- Выбираем "Build and deploy from a Git repository"
- Подключаем GitHub аккаунт
- Выбираем репозиторий с ботом

### 3. **Настройки деплоя**
```
Name: black-russia-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

### 4. **Переменные окружения**
В разделе "Environment Variables" добавляем:
```
BOT_TOKEN = 8172843951:AAFHMnhFITsIlnA9EwgpVenTHg47UO64bys
```

### 5. **Деплой**
- Нажимаем "Create Web Service"
- Ждем завершения сборки (2-3 минуты)
- Бот автоматически запустится!

## ✅ **Преимущества Render:**
- 🆓 **Бесплатно навсегда**
- 🔄 **Автоматическое обновление** из GitHub
- ⚡ **Быстрый и надежный**
- 🚫 **Не засыпает** (работает 24/7)
- 🔧 **Простая настройка**

## 🔗 **После деплоя:**
- Render даст URL типа: `https://black-russia-bot.onrender.com`
- Бот будет работать по этому адресу
- При каждом push в GitHub - автоматическое обновление!

## 🎯 **Готово!**
Твой бот будет работать 24/7 бесплатно навсегда! 🎉
