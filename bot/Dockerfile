# Используем Python
FROM python:3.14-slim

# Рабочая директория
WORKDIR /app

# Копируем только файлы зависимостей
COPY bot/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY bot/ ./bot/

# Экспорт переменных окружения из .env (если нужно, можно копировать)
# COPY .env .env

# Запуск notify server + бота через main.py
CMD ["python", "-m", "bot.main"]
