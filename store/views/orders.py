from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from store.models.product import Product
from store.models.brand import *
from store.models.category import *
from store.models.orders import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def delete(request, id):
    if request.method=='POST':
        order=Order.objects.filter(id=id)
        order.delete()
        return redirect('orders')



    

@login_required(login_url='login')
def orders(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    customer = request.session.get('customer')
    orders = Order.get_orders_by_customer(customer)
    deleteorder=request.GET.get('order')
    order = request.POST.get('order')
    if deleteorder:
        order=Order.objects.filter(id__in=deleteorder)
        product=Order.objects.filter(id__in=order.product.id)
        stock=(product.stock+order.quantity)
        new_product=Product(stock=stock)
        new_product.save()
        order.delete()
        messages.success(request, f'Order for {order}Item Cancelled Successfully')
    print(orders)
    
    return render(request , 'orders.html'  , {'orders' : orders,'orderes':'orderes','productes':productes,'brands':brands,'categories':categories})