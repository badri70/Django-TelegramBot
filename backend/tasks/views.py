from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from rest_framework import status
from .serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskCompleteSerializer,
    CategoryCreateSerializer,
    CategoryListSerializer,
    TelegramAuthSerializer
)
    
from .models import Task, Category, TelegramUser


# Create your views here.
class TelegramAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id = serializer.validated_data["telegram_id"]
        username = serializer.validated_data.get("username", "")

        tg_user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "user": User.objects.create_user(
                    username=f"tg_{telegram_id}"
                ),
                "username": username,
            }
        )

        refresh = RefreshToken.for_user(tg_user.user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "created": created
        })


class TaskViewSet(ModelViewSet):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskListSerializer
        elif self.action == 'complete':
            return TaskCompleteSerializer
        return TaskCreateSerializer    

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        task = self.get_queryset().get(pk=pk)
        task.is_completed = True
        task.save()
        serializer = TaskListSerializer(task)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategoryListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action=='retrieve':
            return CategoryListSerializer
        return CategoryCreateSerializer 

    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)