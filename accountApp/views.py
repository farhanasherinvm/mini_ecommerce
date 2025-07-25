from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerialization, ProductModelSerialization, CategoryModelSerialization, CartModelSerialization
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . models import ProductModel, CategoryModel, CartModel
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

# User authentication and authorizations
class UserRegistrationView(GenericAPIView):
    def post(self, request):
        obj = UserSerialization(data=request.data)
        obj.is_valid(raise_exception=True)
        obj.save()
        return Response({"message":"User registered successfully"},  status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(GenericAPIView):
    def post(self, request):
        x = Response()
        x.delete_cookie('refresh')
        x.delete_cookie('access')
        x.data = {
            "message":"User logout succesfully"
        }
        return x


# Add categories
class AddCategory(GenericAPIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        category = CategoryModelSerialization(data=request.data)
        category.is_valid(raise_exception=True)
        category.save()
        return Response(category.data)

# List all categories
class ListCategories(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategoryModelSerialization(categories, many=True)
        return Response(serializer.data)

# Products Adding
class ProductAdd(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        # category = CategoryModel.objects.get(id=request.data['category'])
        # print(category)
        # request.data['category'] = category.name
        serializer = ProductModelSerialization(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer)
        serializer.save()
        return Response(serializer.data)

# Products retrieving
class ProductsList(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerialization
    pagination_class = PageNumberPagination
    def get(self, request):
        products = ProductModel.objects.all()
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request, view=self)
        serializer = ProductModelSerialization(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

# Retrieve each product and manage(only admin)
class ProductDetail(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        product = ProductModel.objects.get(id=id)
        serializer = ProductModelSerialization(product)
        return Response(serializer.data)

    def patch(self, request, id):
        product = ProductModel.objects.get(id=id)
        obj = ProductModelSerialization(
            instance=product, # the record to update
            data=request.data # incoming new values
        )
        if obj.is_valid():
            obj.save()
            return Response("Product updated successfully!")
        else:
            return Response("Failed to update the product")

    def delete(self, request, id):
        product = ProductModel.objects.filter(id=id)
        if not product:
            return Response({"Error":"Product not found"})
        product.delete()
        return Response({"Message":"Product deleted successfully!"})


# Add products to the cart
class AddCart(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = CartModelSerialization(data=request.data)
        cart.is_valid(raise_exception=True)
        cart.save()
        return Response({"message":"Cart added successfully!"})

# Get Carts
class CartDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        carts = CartModel.objects.all()
        serializer = CartModelSerialization(carts, many=True)
        return Response(serializer.data)

    def patch(self, request, id):
        cartItem = CartModel.objects.get(id=id)
        obj = CartModelSerialization(
            instance=cartItem,  # the record to update
            data=request.data  # incoming new values
        )
        if obj.is_valid():
            obj.save()
            return Response("Cart item updated successfully!")
        else:
            return Response("Failed to update the cart")

    def delete(self, request, id):
        cartItem = CartModel.objects.filter(id=id)
        if not cartItem:
            return Response({"Error":"Cart item not found"})
        cartItem.delete()
        return Response({"Message":"Cart deleted successfully!"})




