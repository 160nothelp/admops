from rest_framework import serializers

from .models import Items, ItemPlans


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


class ItemPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPlans
        fields = '__all__'
