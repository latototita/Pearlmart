from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
import random
from Eshop import settings
from store.models.product import Product
from store.models.orders import Order
from store.models.models import *
from store.models.brand import Brand
from store.models.category import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
from .forms import *
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

now = timezone.now() # current date and time


time = now.strftime("%H:%M:%S")


date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


 
@login_required(login_url='login')
def checkout(request):
    brands = Brand.get_all_brand()
    address = request.POST.get('address')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    cart = request.session.get('cart')
    customer = request.user.id
    products = Product.get_products_by_id(list(cart.keys()))
    ordering_code= ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567893456789') for _ in range(6)])
    product_lists=""
    dates=datetime.datetime.today()

    if products:
        total_price=0
        for product in products:
            total_price=int(total_price)+int(product.price)
            
        brands = Brand.get_all_brand()
        categories = Category.get_all_categories()
        fashion_cat=Category.objects.filter(is_tech=True)
        tech_cat=Category.objects.filter(is_fashion=True)
        cat_home=Category.objects.filter(is_home=True)
        party_cat=Category.objects.filter(is_party=True)
        tagged_cat=Category.objects.filter(is_tagged=True)
        context={'product_lists':product_lists,'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'categories':categories,'brands':brands}
        if request.method=='POST':
            total_price=total_price+3000
            form=PaymentForm(request.POST)
            if form.is_valid():
                pm=form.cleaned_data['payment_method']
                payment_method=Method.objects.get(name=pm)
                method=payment_method.name
                if str(method)=='MTN':
                    name=  request.user.username
                    email = email
                    amount = total_price
                    phone = phone
                    if products:
                        total_price=0
                        for product in products:
                            vendor=Vendor.objects.get(vendor=product.shop)
                            order = Order(customer=User(id=customer),
                                        product=product,
                                        dates=dates,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        shop_name=vendor.shop_name,
                                        email=email,
                                        payment_method=payment_method,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            total_price=int(total_price)+int(product.price)
                            order_records = Order_record(customer=request.user.username,
                                        product=product.name,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        email=email,
                                        payment_method=payment_method,
                                        dates=dates,
                                        shop_name=vendor.shop_name,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            order.save()
                            order_records.save()
                            product_stock=Product.objects.get(id=product.id)
                            if (cart.get(str(product.id)))<product_stock.stock:
                                product_stock.stock=(product_stock.stock-cart.get(str(product.id)))
                                product_stock.save()
                            else:
                                send_mail(
                                'Order Made',
                                f'Order less than stock for {product.name} with ID of {product.id}, Please Procure More',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                            quantity=int(cart.get(str(product.id)))
                            
                            total_price=str((product.price*quantity))
                            product_lists+=(str(quantity) +" "+product.name+"(s)"+":\t = "+total_price+"/="+"\n")

                        if email:
                                
                            send_mail(
                                'Order Received  Successfully',
                                f'Your Order with Order Code: {ordering_code} \n For the following Products: \n{product_lists}\nYour Order dearest {request.user.username} Has Been made Successfully.\nYou will be contacted soon by Our delivery team to make deliveries And Collect Payment, Cash On delivery. Keep This Code "\t"  :{ordering_code} \n for security purposes and confirmation of delivery',
                                settings.EMAIL_HOST_USER,
                                [f'{email}'],
                                fail_silently = True,
                            )
                            send_mail(
                                'Order Made',
                                f'Order has been made on at exactly {date_time} Today.\n Kind make th delivery within 24 Hours. \nTo be delivered at {address}, Contact the customer on {phone} \n For the following Orders \n{product_lists}\n',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                        
                        messages.success(request, f'Dear {request.user.username}, \nYour Order For the following Products:\n{product_lists}\n as been Received Successfully, With Order Code {ordering_code} To be use for delivery and security. Now proceed to finsh off payments')
                    return redirect(str(process_payment(name,email,amount,phone,ordering_code)))
                if str(method)=='Airtel':
                    name=  request.user.username
                    email = email
                    amount = total_price
                    phone = phone
                    if products:
                        total_price=0
                        for product in products:
                            vendor=Vendor.objects.get(vendor=product.shop)
                            order = Order(customer=User(id=customer),
                                        product=product,
                                        dates=dates,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        shop_name=vendor.shop_name,
                                        email=email,
                                        payment_method=payment_method,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            total_price=int(total_price)+int(product.price)
                            order_records = Order_record(customer=request.user.username,
                                        product=product.name,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        email=email,
                                        payment_method=payment_method,
                                        dates=dates,
                                        shop_name=vendor.shop_name,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            order.save()
                            order_records.save()
                            product_stock=Product.objects.get(id=product.id)
                            if (cart.get(str(product.id)))<product_stock.stock:
                                product_stock.stock=(product_stock.stock-cart.get(str(product.id)))
                                product_stock.save()
                            else:
                                send_mail(
                                'Order Made',
                                f'Order less than stock for {product.name} with ID of {product.id}, Please Procure More',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                            quantity=int(cart.get(str(product.id)))
                            
                            total_price=str((product.price*quantity))
                            product_lists+=(str(quantity) +" "+product.name+"(s)"+":\t = "+total_price+"/="+"\n")

                        if email:
                                
                            send_mail(
                                'Order Received  Successfully',
                                f'Your Order with Order Code: {ordering_code} \n For the following Products: \n{product_lists}\nYour Order dearest {request.user.username} Has Been made Successfully.\nYou will be contacted soon by Our delivery team to make deliveries And Collect Payment, Cash On delivery. Keep This Code "\t"  :{ordering_code} \n for security purposes and confirmation of delivery',
                                settings.EMAIL_HOST_USER,
                                [f'{email}'],
                                fail_silently = True,
                            )
                            send_mail(
                                'Order Made',
                                f'Order has been made on at exactly {date_time} Today.\n Kind make th delivery within 24 Hours. \nTo be delivered at {address}, Contact the customer on {phone} \n For the following Orders \n{product_lists}\n',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                        
                        messages.success(request, f'Dear {request.user.username}, \nYour Order For the following Products:\n{product_lists}\n as been Received Successfully, With Order Code {ordering_code} To be use for delivery and security. Now proceed to finsh off payments')
                    return redirect(str(process_payment(name,email,amount,phone,ordering_code)))
                if str(method)=='Visa':
                    name=  request.user.username
                    email = email
                    amount = total_price
                    phone = phone
                    if products:
                        total_price=0
                        for product in products:
                            vendor=Vendor.objects.get(vendor=product.shop)
                            order = Order(customer=User(id=customer),
                                        product=product,
                                        dates=dates,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        shop_name=vendor.shop_name,
                                        email=email,
                                        payment_method=payment_method,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            total_price=int(total_price)+int(product.price)
                            order_records = Order_record(customer=request.user.username,
                                        product=product.name,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        email=email,
                                        payment_method=payment_method,
                                        dates=dates,
                                        shop_name=vendor.shop_name,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            order.save()
                            order_records.save()
                            product_stock=Product.objects.get(id=product.id)
                            if (cart.get(str(product.id)))<product_stock.stock:
                                product_stock.stock=(product_stock.stock-cart.get(str(product.id)))
                                product_stock.save()
                            else:
                                send_mail(
                                'Order Made',
                                f'Order less than stock for {product.name} with ID of {product.id}, Please Procure More',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                            quantity=int(cart.get(str(product.id)))
                            
                            total_price=str((product.price*quantity))
                            product_lists+=(str(quantity) +" "+product.name+"(s)"+":\t = "+total_price+"/="+"\n")

                        if email:
                                
                            send_mail(
                                'Order Received  Successfully',
                                f'Your Order with Order Code: {ordering_code} \n For the following Products: \n{product_lists}\nYour Order dearest {request.user.username} Has Been made Successfully.\nYou will be contacted soon by Our delivery team to make deliveries And Collect Payment, Cash On delivery. Keep This Code "\t"  :{ordering_code} \n for security purposes and confirmation of delivery',
                                settings.EMAIL_HOST_USER,
                                [f'{email}'],
                                fail_silently = True,
                            )
                            send_mail(
                                'Order Made',
                                f'Order has been made on at exactly {date_time} Today.\n Kind make th delivery within 24 Hours. \nTo be delivered at {address}, Contact the customer on {phone} \n For the following Orders \n{product_lists}\n',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                        
                        messages.success(request, f'Dear {request.user.username}, \nYour Order For the following Products:\n{product_lists}\n as been Received Successfully, With Order Code {ordering_code} To be use for delivery and security. Now proceed to finsh off payments')
                        request.session['cart'] = {}
                    return redirect(str(process_payment_visa(name,email,amount,phone,ordering_code)))
                if str(method)=='Cryptocurrency':
                    request.session['total_price'] = f'{total_price}'
                    request.session['ordering_code'] = f'{ordering_code}'
                    request.session['phone'] = f'{phone}'
                    request.session['customer'] = f'{request.user.id}'
                    request.session['dates'] = f'{dates}'
                    if products:
                        total_price=0
                        for product in products:
                            vendor=Vendor.objects.get(vendor=product.shop)
                            order = Order(customer=User(id=customer),
                                        product=product,
                                        dates=dates,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        shop_name=vendor.shop_name,
                                        email=email,
                                        payment_method=payment_method,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            total_price=int(total_price)+int(product.price)
                            order_records = Order_record(customer=request.user.username,
                                        product=product.name,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        email=email,
                                        payment_method=payment_method,
                                        dates=dates,
                                        shop_name=vendor.shop_name,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            order.save()
                            order_records.save()
                            product_stock=Product.objects.get(id=product.id)
                            if (cart.get(str(product.id)))<product_stock.stock:
                                product_stock.stock=(product_stock.stock-cart.get(str(product.id)))
                                product_stock.save()
                            else:
                                send_mail(
                                'Order Made',
                                f'Order less than stock for {product.name} with ID of {product.id}, Please Procure More',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                            quantity=int(cart.get(str(product.id)))
                            
                            total_price=str((product.price*quantity))
                            product_lists+=(str(quantity) +" "+product.name+"(s)"+":\t = "+total_price+"/="+"\n")

                        if email:
                                
                            send_mail(
                                'Order Received  Successfully',
                                f'Your Order with Order Code: {ordering_code} \n For the following Products: \n{product_lists}\nYour Order dearest {request.user.username} Has Been made Successfully.\nYou will be contacted soon by Our delivery team to make deliveries And Collect Payment, Cash On delivery. Keep This Code "\t"  :{ordering_code} \n for security purposes and confirmation of delivery',
                                settings.EMAIL_HOST_USER,
                                [f'{email}'],
                                fail_silently = True,
                            )
                            send_mail(
                                'Order Made',
                                f'Order has been made on at exactly {date_time} Today.\n Kind make th delivery within 24 Hours. \nTo be delivered at {address}, Contact the customer on {phone} \n For the following Orders \n{product_lists}\n',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                        
                        
                        messages.success(request, f'Dear {request.user.username}, \nYour Order For the following Products:\n{product_lists}\n as been Received Successfully, With Order Code {ordering_code} To be use for delivery and security. Now proceed to finsh off payments')
                    return redirect('home_view')
                if str(method)=='Cash_on_Delivery':
                    print('Cash')
                    if products:
                        total_price=0
                        for product in products:
                            vendor=Vendor.objects.get(vendor=product.shop)
                            order = Order(customer=User(id=customer),
                                        product=product,
                                        dates=dates,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        shop_name=vendor.shop_name,
                                        email=email,
                                        payment_method=payment_method,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            total_price=int(total_price)+int(product.price)
                            order_records = Order_record(customer=request.user.username,
                                        product=product.name,
                                        price=product.price,
                                        selling_price=product.selling_price,
                                        address=address,
                                        phone=phone,
                                        email=email,
                                        payment_method=payment_method,
                                        dates=dates,
                                        shop_name=vendor.shop_name,
                                        ordering_code=ordering_code,
                                        quantity=cart.get(str(product.id)))
                            order.save()
                            order_records.save()
                            product_stock=Product.objects.get(id=product.id)
                            if (cart.get(str(product.id)))<product_stock.stock:
                                product_stock.stock=(product_stock.stock-cart.get(str(product.id)))
                                product_stock.save()
                            else:
                                send_mail(
                                'Order Made',
                                f'Order less than stock for {product.name} with ID of {product.id}, Please Procure More',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                            quantity=int(cart.get(str(product.id)))
                            
                            total_price=str((product.price*quantity))
                            product_lists+=(str(quantity) +" "+product.name+"(s)"+":\t = "+total_price+"/="+"\n")

                        if email:
                                
                            send_mail(
                                'Order Received  Successfully',
                                f'Your Order with Order Code: {ordering_code} \n For the following Products: \n{product_lists}\nYour Order dearest {request.user.username} Has Been made Successfully.\nYou will be contacted soon by Our delivery team to make deliveries And Collect Payment, Cash On delivery. Keep This Code "\t"  :{ordering_code} \n for security purposes and confirmation of delivery',
                                settings.EMAIL_HOST_USER,
                                [f'{email}'],
                                fail_silently = True,
                            )
                            send_mail(
                                'Order Made',
                                f'Order has been made on at exactly {date_time} Today.\n Kind make th delivery within 24 Hours. \nTo be delivered at {address}, Contact the customer on {phone} \n For the following Orders \n{product_lists}\n',
                                settings.EMAIL_HOST_USER,
                                ['pearlmartbusinesses@gmail.com'],
                                fail_silently = True,
                            )
                        
                        
                        messages.success(request, f'Dear {request.user.username}, \nYour Order For the following Products:\n{product_lists}\n as been Received Successfully, With Order Code {ordering_code} To be use for delivery and security. Delivery will be made Soon')
                        request.session['cart'] = {}
                        return render(request, 'success.html',context)
        return render(request, 'success.html',context)
    else:
        messages.success(request, f'You Have an empty Cart, Please Add Orders to Cart and Make Your Order')
        return redirect('checkout1')

import math,requests

def process_payment(name,email,amount,phone,ordering_code):
     auth_token= 'FLWSECK_TEST-9d95ef51f2cff0ee18cb3377923e8095-X'
     request.session['cart'] = {}
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":ordering_code,
                "amount":amount,
                "currency":"UGX",

                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"mobilemoneyuganda",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Pearlmart",
                    "description":"Your loyal online Market",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link

def process_payment_visa(name,email,amount,phone,ordering_code):
     auth_token= 'FLWSECK_TEST-9d95ef51f2cff0ee18cb3377923e8095-X'
     request.session['cart'] = {}
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":ordering_code,
                "amount":amount,
                "currency":"UGX",

                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Pearlmart",
                    "description":"Your loyal online Market",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    if status==SUCCESSFUL:
        messages.success(request, 'Verified Successful')
    else:
        messages.error(request, 'Verified Failed')
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')
