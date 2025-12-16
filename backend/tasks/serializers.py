from rest_framework import serializers
from .models import Category, Task


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'categories']
        

class TaskListSerializer(serializers.ModelSerializer):
    
    class Meta:
        depth = 1
        model = Task
        exclude = ['user']
        
    
class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_completed']  # только это поле

    def update(self, instance, validated_data):
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance
