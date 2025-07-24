from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerialization, ProductModelSerialization, CategoryModelSerialization
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from . models import ProductModel

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
    def post(self, request):
        category = CategoryModelSerialization(data=request.data)
        category.is_valid(raise_exception=True)
        return Response(category.data)

# Products Adding
class ProductAdd(GenericAPIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductModelSerialization(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Products retrieving
class ProductsList(GenericAPIView):
    def get(self, request):
        products = ProductModel.objects.all()
        serializer = ProductModelSerialization(products, many=True)
        return Response(serializer.data)

# Retrieve each product and manage(only admin)
class ProductDetail(GenericAPIView):
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
        product = ProductModel.objects.filter(id)
        if not product:
            return Response({"Error":"Product not found"})
        product.delete()
        return Response({"Message":"Product deleted successfully!"})




