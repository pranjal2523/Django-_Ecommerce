from django.urls import path
from . import views

app_name = 'app_cart'

urlpatterns = [
    path('atc/<pk>/', views.a_t_c, name='atc'),
    path('cart/', views.cart_v, name='cart'), 
    path('remove/<pk>/', views.r_f_c, name='remove'), 
    path('inc/<pk>/', views.inc_cart, name='inc'), 
    path('dec/<pk>/', views.dec_cart, name='dec'), 


]