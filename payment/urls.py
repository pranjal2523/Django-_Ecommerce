from django.urls import path
from payment import views

app_name = "payment"

urlpatterns=[
    path('checkout/', views.checkout, name="checkout"), 
    
    path('pay/', views.payment, name="pay"),
    path('complete/', views.complete, name="complete"),
    path('purchased/<tran_id>/', views.purchased, name="purchased"), 
    path('orders/', views.order_view, name="orders"), 
]