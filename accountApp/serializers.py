from rest_framework import serializers
from .models import User, ProductModel, CategoryModel, CartModel

class UserSerialization(serializers.ModelSerializer):
    confirmpassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmpassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmpassword')  # Exclude from saving
        # Extract the password field from validated_data, if present
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CategoryModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"
class ProductModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

class CartModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = "__all__"