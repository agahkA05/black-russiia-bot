@echo off
echo Обновление бота на хостинге...

echo Добавление изменений в Git...
git add .

echo Ввод сообщения коммита...
set /p message="Введите описание изменений: "

echo Создание коммита...
git commit -m "%message%"

echo Отправка на GitHub...
git push origin main

echo.
echo ✅ Обновление отправлено!
echo 🚀 Railway автоматически обновит бота через 1-2 минуты
echo.
echo Проверить статус можно на: https://railway.app/dashboard
echo.
pause

