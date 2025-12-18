import requests
from celery import shared_task
from django.utils import timezone
from .models import Task
from dotenv import load_dotenv
import os

load_dotenv()
BOT_NOTIFY_URL = os.getenv('BOT_NOTIFY_URL', 'http://localhost:8001/notify')

@shared_task
def notify_due_tasks():
    now = timezone.now()
    tasks = Task.objects.filter(due_date__lte=now, is_completed=False)

    for task in tasks:
        try:
            tg_user = getattr(task.user, "telegramuser", None)
            if not tg_user:
                continue

            requests.post(BOT_NOTIFY_URL, json={
                "telegram_id": tg_user.telegram_id,
                "task_title": task.title,
                "task_id": task.id,
            })
        except Exception as e:
            print(f"Error sending notify for task {task.id}: {e}")

    print(f"Checked for due tasks at {now}. Found {tasks.count()} due tasks.")
