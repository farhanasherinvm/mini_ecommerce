from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "username", "password"]


class CategoryModel(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    price = models.CharField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)