from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, TelegramAuthView


router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("auth/telegram/", TelegramAuthView.as_view()),
]
