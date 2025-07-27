from rest_framework import serializers
from .models import User, ProductModel, CategoryModel, CartModel

class UserSerialization(serializers.ModelSerializer):
    confirmpassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','username','phone', 'email','confirmpassword')

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
        fields = ('id', 'name')

class ProductModelSerialization(serializers.ModelSerializer):
    category = CategoryModelSerialization(read_only=True)

    cat_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoryModel.objects.all(), write_only=True, source='category'
    )
    class Meta:
        model = ProductModel
        fields = ('cat_id','id', 'name', 'price','description', 'stock', 'category')

class CartModelSerialization(serializers.ModelSerializer):
    user = UserSerialization(read_only=True)
    product = ProductModelSerialization(read_only=True)

    # These are used when creating/updating
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductModel.objects.all(), write_only=True, source='product'
    )
    class Meta:
        model = CartModel
        fields = "__all__"