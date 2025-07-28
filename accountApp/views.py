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
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response = Response({
                "message":"User logged in successfully",
                'access': str(access_token)
            }, status=status.HTTP_200_OK)

            # Set refresh token in HttpOnly cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                max_age=86400, #1 day  #the number of seconds until the cookie expires
                secure=True, #the cookie will only be sent over HTTPS connections
                httponly=True,
                samesite='Lax'
            )
            return response

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
        if category.is_valid():
            category.save()
            return Response({
                "status": "success",
                "message": "Added a new category!",
                "data": category.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "failed",
                "message": "failed to add category",
                "error": category.errors
            }, status=status.HTTP_400_BAD_REQUEST)

# List all categories
class ListCategories(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategoryModelSerialization(categories, many=True)

        return Response({
            "status": "success",
            "message": "Fetched all available categories from the cart",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# Products Adding
class ProductAdd(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        # category = CategoryModel.objects.get(id=request.data['category'])
        # print(category)
        # request.data['category'] = category.name
        serializer = ProductModelSerialization(data=request.data)
        if serializer.is_valid():
            # print(serializer)
            serializer.save()
            return Response({
                "status":"success",
                "message":"Product added to the table",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status":"failed",
                "message":"failed to add product",
                "error":serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

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

        return Response({
            "status":"success",
            "message":"Fetched the product",
            "data":serializer.data
        }, status=status.HTTP_200_OK)


    def patch(self, request, id):
        product = ProductModel.objects.get(id=id)
        obj = ProductModelSerialization(
            instance=product, # the record to update
            data=request.data # incoming new values
        )
        if obj.is_valid():
            obj.save()
            return Response({
                "status":"success",
                "message":"Product updated successfully!",
                "data":obj.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status":"failed",
                "message":"Failed to update the product",
                "error":obj.errors
            })

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
        if cart.is_valid():
            cart.save()
            return Response({
                "status":"success",
                "message":"Cart added successfully!",
                "data":cart.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status":"Failed",
                "message":"Failed to add the cart",
                "error":cart.errors
            }, status=status.HTTP_400_BAD_REQUEST)

# Get Carts
class CartDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        carts = CartModel.objects.filter(user=request.user)
        serializer = CartModelSerialization(carts, many=True)

        return Response({
            "status":"success",
            "message":"Fetched all data from the cart",
            "data":serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        cartItem = CartModel.objects.get(id=id)
        obj = CartModelSerialization(
            instance=cartItem,  # the record to update
            data=request.data  # incoming new values
        )
        if obj.is_valid():
            obj.save()
            return Response({
                "status":"success",
                "message":"Cart item updated successfully!",
                "data":obj.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status":"failed",
                "message":"Failed to update the cart",
                "error":obj.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        cartItem = CartModel.objects.filter(id=id)
        if not cartItem:
            return Response({"Error":"Cart item not found"}, status=status.HTTP_400_BAD_REQUEST)
        cartItem.delete()
        return Response({"Message":"Cart deleted successfully!"}, status=status.HTTP_200_OK)




