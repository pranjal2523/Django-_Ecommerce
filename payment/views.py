from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from payment.models import BillAdd
from payment.forms import Billform

from app_cart.models import Order, cart

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#For Payment
from sslcommerz_lib import SSLCOMMERZ 



SID = "abeds6401ce5c930e7",
KEY = "abeds6401ce5c930e7@ssl",

@login_required
def checkout(request):
    saved_add = BillAdd.objects.get_or_create(user=request.user)
    saved_add = saved_add[0]
    form = Billform(instance=saved_add)
    if request.method =='POST':
        form = Billform(request.POST, instance=saved_add)
        if form.is_valid():
            form.save()
            form = Billform(instance=saved_add)
            messages.success(request, "Shipping Address Saved!")

    order_qs = Order.objects.filter(user= request.user, ordered = False)
    order_item = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_total()

    return render(request, 'payment/checkout.html', context={'form':form, 'total':order_total, 'order_items': order_item, 'saved_add': saved_add })


@login_required
def payment(request):
    saved_address =  BillAdd.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, "Please complete Shipping Address") 
        return redirect("payment:checkout")
    
    if not request.user.profile.is_fully_filled(): 
        messages.info(request, "Please complete profile details") 
        return redirect("app_login:change_profile")
    #return render(request, "payment/payment.html", context={})
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    order_item = order_qs[0].orderitems.all()
    order_quant = order_qs[0].orderitems.count()
    order_total =  order_qs[0].get_total()
    status_url = request.build_absolute_uri(reverse("payment:complete"))
    print(status_url)
    settings = { 'store_id': SID, 'store_pass': KEY, 'issandbox': True }
    cur_user = request.user
    sslcommez = SSLCOMMERZ(settings)
    #print(sslcommez)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "INR"
    post_body['tran_id'] = "comerce01"
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = cur_user.profile.full_name
    post_body['cus_email'] = cur_user.email
    post_body['cus_phone'] = cur_user.profile.phone
    post_body['cus_add1'] = cur_user.profile.address_1
    post_body['cus_city'] = cur_user.profile.city
    post_body['cus_country'] = cur_user.profile.country
    post_body['shipping_method'] = "courier"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = order_quant
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"
    post_body['ship_name'] = cur_user.profile.full_name
    post_body['ship_add1'] = cur_user.profile.address_1
    post_body['ship_city'] = cur_user.profile.city
    post_body['ship_country'] = cur_user.profile.country
    post_body['ship_postcode'] = cur_user.profile.zipcode

    

    response = sslcommez.createSession(post_body)
    
    
    return redirect(response['redirectGatewayURL'])




@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == "post":
        pay_data = request.POST
        status = pay_data['status']

        if status == 'VALID':
            v_id = pay_data['val_id']
            tran_id  = pay_data['bank_tran_id']             
            messages.success(request, "Your payment is successfull")
            return HttpResponseRedirect(reverse("payment:purchased", kwargs={'tran_id':tran_id,}))
        elif status == 'FAILED':
            messages.success(request, "Your payment is Unsuccessfull")
    #return redirect("app_shop:home")
    return render(request, 'payment/complete.html')


@login_required
def purchased(request, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderid = tran_id
    order.ordered = True
    order.orderid = orderid
    order.save()

    cart_item = cart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()


    return HttpResponseRedirect(reverse("app_shop:home"))


@login_required
def order_view(request):
    try:
        order = Order.objects.filter(user=request.user, ordered= True)
        context = {"orders": order}
        if order[0].orderitems.count() == 0:
            raise Exception
    except:
        messages.warning(request, "You dont have any Order!")
        return redirect("app_shop:home")
    return render(request, "payment/order.html", context)