from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_id', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at']
      
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']
        read_only_fields = ['user']
