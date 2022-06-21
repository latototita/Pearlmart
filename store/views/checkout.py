from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
import random
from Eshop import settings
from store.models.product import Product
from store.models.orders import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
from django.utils import timezone
now = timezone.now() # current date and time


time = now.strftime("%H:%M:%S")


date_time = now.strftime("%m/%d/%Y, %H:%M:%S")



@login_required(login_url='login')
def checkout(request):
    address = request.POST.get('address')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    cart = request.session.get('cart')
    customer = request.session.get('customer')
    products = Product.get_products_by_id(list(cart.keys()))
    print(address, phone, customer, cart, products)
    ordering_code= ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567893456789') for _ in range(6)])

    for product in products:
        print(cart.get(str(product.id)))
        order = Order(customer=User(id=customer),
                      product=product,
                      price=product.price,
                      selling_price=product.selling_price,
                      address=address,
                      phone=phone,
                      email=email,
                      ordering_code=ordering_code,
                      quantity=cart.get(str(product.id)))
        order.save()
    if email:
            
        send_mail(
            'That’s your subject',
            f'Your Order with Order Code   >>{ordering_code}<<   Has Been made Successfully.You will be contacted soon by Our delivery team to make deliveries And Collect Payment, Cash On delivery. Keep This Code   >>{ordering_code}<<   for security purposes and confirmation of delivery',
            settings.EMAIL_HOST_USER,
            [f'{email}'],
            fail_silently = False,
        )
    send_mail(
            'Order Made',
            f'Order has been made on at exactly {date_time} Today. Kind make th delivery within 24 Hours. To be delivered at {address}, Contact the customer on {phone}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = False,
        )
    
    messages.success(request, f'Dear Customer Your Order as been Recived  Successfully, Will be delivered To {address} within 24 hours, With Order Code {ordering_code} To be use for delivery and security. Have a Good Day.Take Care')
    request.session['cart'] = {}
    return redirect('store')
