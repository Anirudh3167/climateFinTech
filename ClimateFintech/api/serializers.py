from rest_framework import serializers
from Backend.models import CartItems

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'