# Django-TelegramBot

Проект представляет собой систему для управления задачами с **Django Backend** и **Telegram Bot**, которая позволяет создавать, просматривать и завершать задачи, а также получать уведомления о сроках выполнения через Telegram.

## Функциональность

- Регистрация и авторизация пользователей
- CRUD для задач:
  - Создание задач
  - Просмотр списка задач
  - Завершение задачи
- Категории задач
- Уведомления о просроченных задачах через Telegram Bot
- Асинхронная обработка уведомлений через Celery + Redis

## Технологии

**Backend:**
- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL
- Celery
- Redis

**Bot:**
- Python 3.14
- Aiogram 3.x
- Aiogram-dialog
- aiohttp

**Docker:**
- Docker
- Docker Compose

## Структура проекта

```bash
project/
│
├─ backend/ # Django backend
│ ├─ Dockerfile # Для backend
│ ├─ requirements.txt # список зависимостей для backend
│ ├─ manage.py # Для запуска приложения
│ ├─ tasks/ # Приложение для управления задачами
│ └─ core/ # Главная директория со всеми настройками
│
├─ bot/ # Telegram Bot сервис
│ ├─ requirements.txt # список зависимостей для bot
│ ├─ api/ # для связки с backend
│ ├─ Dockerfile.bot # Для бота
│ ├─ storage/ # для хранения временных данных
│ ├─ handlers/ # Обработчики команд и callback
│ ├─ dialogs/ # Диалоги aiogram-dialog
│ ├─ config.py # Для импорта всех ключевых значений из .env файла
│ ├─ notify_service.py # HTTP-сервис для отправки уведомлений
│ └─ main.py # Точка запуска бота
└─docker-compose.yml
```

## Установка и запуск

### 1. Клонируем репозиторий

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Настройка .env файла

Создайте файл .env в корне проекта и добавьте:

```env
# Django settings
DEBUG=True
SECRET_KEY=django-insecure-)c0^&l$a4wiiju^hxzj&n9z%!ati0uu7a*xxhp@z#)870w6c+@
API_URL=http://backend:8000/api

# Database settings
POSTGRES_DB=authz
POSTGRES_USER=authz_user
POSTGRES_PASSWORD=authz_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Celery settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Bot settings
BOT_TOKEN=8583654438:AAEfF2J93Gxf4VfXqCmbwzs_wsUhK7-cCEg
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
BOT_NOTIFY_URL=http://bot:8001/notify

# Other settings
TIME_ZONE=America/Adak
```

### 3. Запуск через Docker Compose
```bash
docker-compose up --build
```

Это создаст и запустит:

- Backend Django (http://localhost:8000)

- Telegram Bot

- Redis

- PostgreSQL

- Celery Worker

### 4. Использование бота

После запуска:

1. Найдите бота в Telegram.

2. Введите команду /start — появится клавиатура:

- /tasks — показать задачи

- /add_task — создать задачу

- /categories — список категорий

- /add_category — добавить категорию

3. Если задача просрочена, придет уведомление с кнопкой для завершения.
