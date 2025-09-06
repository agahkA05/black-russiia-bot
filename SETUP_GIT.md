# Настройка Git и автодеплоя

## 📥 Шаг 1: Установка Git

1. **Скачай Git:** https://git-scm.com/download/win
2. **Установи** с настройками по умолчанию
3. **Перезапусти** командную строку

## 🔧 Шаг 2: Настройка Git

```bash
# Настрой имя и email
git config --global user.name "Твое Имя"
git config --global user.email "твой@email.com"
```

## 🚀 Шаг 3: Создание репозитория

1. **Создай репозиторий** на GitHub:
   - Иди на https://github.com
   - Нажми "New repository"
   - Назови: `black-russia-bot`
   - Сделай публичным
   - НЕ добавляй README, .gitignore, лицензию

2. **Инициализируй Git** в папке проекта:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/твой-username/black-russia-bot.git
git push -u origin main
```

## ⚙️ Шаг 4: Настройка Railway

1. **Иди на** https://railway.app
2. **Войди** через GitHub
3. **Создай проект:**
   - New Project → Deploy from GitHub repo
   - Выбери `black-russia-bot`
   - Нажми Deploy

4. **Настрой переменные:**
   - Variables → Add Variable
   - `BOT_TOKEN` = `8172843951:AAFHMnhFITsIlnA9EwgpVenTHg47UO64bys`
   - `ADMIN_USERNAME` = `Aga_05`

## 🔄 Шаг 5: Автодеплой готов!

Теперь когда ты:
1. **Меняешь код**
2. **Запускаешь** `quick_update.bat`
3. **Бот автоматически** обновляется на хостинге!

## 📁 Файлы для обновления:

- `quick_update.bat` - быстрое обновление
- `update.bat` - обновление с описанием
- `.github/workflows/deploy.yml` - настройки автодеплоя
- `railway.json` - конфигурация Railway

## 🎯 Результат:

- ✅ Бот работает 24/7 на Railway
- ✅ Автоматические обновления
- ✅ Бесплатно навсегда
- ✅ Простое управление через скрипты

