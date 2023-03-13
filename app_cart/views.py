from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from app_cart.models import cart, Order
from app_shop.models import Product

from django.contrib import messages
# Create your views here.


@login_required
def a_t_c(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = cart.objects.get_or_create(item = item, user = request.user, purchased= False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "this item quantity is updated")
            return redirect('app_shop:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item is added to your cart")
            return redirect("app_shop:home")
    else:
        order = Order(user= request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item is added to your cart")
        return redirect("app_shop:home" )
    
@login_required
def cart_v(request):
    carts = cart.objects.filter(user= request.user, purchased= False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'app_cart/cart.html', context={'carts': carts, 'orders':order})
    
    else:
        messages.warning(request, "You dont have any item in your cart")
        return redirect("app_shop:home")
    

@login_required
def r_f_c(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item = item).exists():
            order_item = cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your cart")
            return redirect("app_cart:cart")
        else:
            messages.info(request, "this item was not in your cart!")
            return redirect("app_shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("app_shop:home")
    

@login_required
def inc_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item= cart.objects.filter(item=item, user= request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("app_cart:cart")
            else:
                messages.info(request, f"{item.name} is not in your cart")
                return redirect("app_shop:home")
        else:
            messages.info(request, "item is not in cart!")
            return redirect("app_shop:home")

@login_required
def dec_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user= request.user, ordered= False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = cart.objects.filter(item= item, user=request.user, purchased=False)[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity updated") 
                return redirect("app_cart:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request, f"{item.name} is removed from your cart")
                return redirect("app_shop:home")
        else:
            messages.info(request,"Your cart is empty")
            return redirect("app_shop:home")