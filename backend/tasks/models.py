from django.db import models
import time
import datetime
from django.contrib.auth.models import User

# Create your models here.
def generate_id():
    return int(time.time() * 1000)


class BaseModel(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        default=generate_id,
        editable=False
    )

    class Meta:
        abstract = True
    

class TelegramUser(BaseModel):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.telegram_id)


class Category(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="categories"
    )
    
    def __str__(self):
        return self.name
    

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title