from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from app_shop.models import Product

# Create your views here.

class home(ListView):
    model = Product
    template_name = 'app_shop/index.html'

class Product( DetailView):
    model = Product
    template_name = 'app_shop/productpage.html'