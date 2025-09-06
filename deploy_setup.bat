@echo off
echo Настройка для деплоя на Railway...

echo Инициализация Git репозитория...
git init

echo Добавление всех файлов...
git add .

echo Первый коммит...
git commit -m "Initial commit - Black Russia Market Bot"

echo.
echo Готово! Теперь:
echo 1. Создайте репозиторий на GitHub
echo 2. Подключите его к Railway
echo 3. Настройте переменные окружения
echo 4. Деплойте!
echo.
pause

