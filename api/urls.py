from django.urls import path
from . import views

app_name = 'app_cart'

urlpatterns = [
   path('article/', views.articleLV.as_view(), name='article'), 
   path('article/<int:pk>', views.articleDV.as_view()), 
   path('create', views.create, name='create'), 

]