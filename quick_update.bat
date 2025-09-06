@echo off
echo 🔄 Быстрое обновление бота...

echo 📝 Добавляем изменения в Git...
git add .

echo 💾 Сохраняем изменения...
git commit -m "Обновление бота: исправлен Railway health check, убрана лишняя информация"

echo 🚀 Отправляем на GitHub...
git push origin main

echo ✅ Обновление завершено!
echo 🌐 Railway автоматически обновит бота через несколько минут
echo 📊 Проверьте статус на https://railway.app

pause