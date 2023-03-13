from django.urls import path
from app_shop import views

app_name = 'app_shop'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('product/<pk>/', views.Product.as_view(), name='product'),

]