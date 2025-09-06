@echo off
echo 🚀 Деплой на Render...
echo.

echo 📦 Добавляем файлы в Git...
git add .

echo 💾 Коммитим изменения...
git commit -m "Обновление бота для Render"

echo 🚀 Отправляем на GitHub...
git push origin main

echo.
echo ✅ Готово! Теперь иди на render.com и создавай Web Service!
echo.
echo 📋 Что делать дальше:
echo 1. Зайди на render.com
echo 2. Создай новый Web Service
echo 3. Подключи GitHub репозиторий
echo 4. Добавь переменную BOT_TOKEN
echo 5. Нажми Deploy!
echo.
pause
