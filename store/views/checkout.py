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
from django.utils import timezone
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
    if products:
        for product in products:
            vendor=Vendor.objects.get(vendor=product.shop)
            order = Order(customer=User(id=customer),
                          product=product,
                          price=product.price,
                          selling_price=product.selling_price,
                          address=address,
                          phone=phone,
                          shop_name=vendor.shop_name,
                          email=email,
                          ordering_code=ordering_code,
                          quantity=cart.get(str(product.id)))
            

            order_records = Order_record(customer=request.user.username,
                          product=product.name,
                          price=product.price,
                          selling_price=product.selling_price,
                          address=address,
                          phone=phone,
                          email=email,
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
                fail_silently = False,
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
                fail_silently = False,
            )
            send_mail(
                'Order Made',
                f'Order has been made on at exactly {date_time} Today.\n Kind make th delivery within 24 Hours. \nTo be delivered at {address}, Contact the customer on {phone} \n For the following Orders \n{product_lists}\n',
                settings.EMAIL_HOST_USER,
                ['pearlmartbusinesses@gmail.com'],
                fail_silently = False,
            )
        
        messages.success(request, f'Dear Customer, \nYour Order For the following Products:\n{product_lists}\n as been Received Successfully, Will be delivered To {address} within 24 hours, With Order Code {ordering_code} To be use for delivery and security. Have a Good Day.Take Care')
        request.session['cart'] = {}
        brands = Brand.get_all_brand()
        categories = Category.get_all_categories()
        fashion_cat=Category.objects.filter(is_tech=True)
        tech_cat=Category.objects.filter(is_fashion=True)
        cat_home=Category.objects.filter(is_home=True)
        party_cat=Category.objects.filter(is_party=True)
        tagged_cat=Category.objects.filter(is_tagged=True)
        context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'product_list' : product_list,'categories':categories,'brands':brands}
        return render(request, 'success.html',context)
    else:
        messages.success(request, f'You Have an empty Cart, Please Add Orders to Cart and Make Your Order')
        return redirect('checkout1')
