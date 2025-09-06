@echo off
echo 🚀 Загрузка в GitHub...
echo.

echo 📦 Добавляем все файлы...
git add .

echo 💾 Создаем коммит...
git commit -m "Обновление бота для Render - готов к деплою"

echo 🚀 Отправляем на GitHub...
git push origin main

echo.
echo ✅ Готово! Все загружено в GitHub!
echo.
echo 🎯 Теперь можно деплоить на Render:
echo 1. Зайди на render.com
echo 2. Создай новый Web Service
echo 3. Подключи GitHub репозиторий
echo 4. Добавь переменную BOT_TOKEN
echo 5. Нажми Deploy!
echo.
pause
