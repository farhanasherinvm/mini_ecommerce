from django.urls import path
from . import views

urlpatterns = [
    path("UserRegistrationView/", views.UserRegistrationView.as_view()),
    path("LoginView/", views.LoginView.as_view()),
    path("UserLogoutView/", views.UserLogoutView.as_view()),

    path("AddCategory/", views.AddCategory.as_view()),
    path("ListCategories/", views.ListCategories.as_view()),
    path("ProductAdd/", views.ProductAdd.as_view()),
    path("ProductsList/", views.ProductsList.as_view()),
    path("ProductDetail/<int:id>/", views.ProductDetail.as_view()),

    path("AddCart/", views.AddCart.as_view()),
    path("CartDetails/", views.CartDetails.as_view()),
    path("CartDetails/<int:id>/", views.CartDetails.as_view())
]