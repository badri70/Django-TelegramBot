from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskCompleteSerializer,
    CategoryCreateSerializer,
    CategoryListSerializer
)
    
from .models import Task, Category


# Create your views here.
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