from django.shortcuts import render , redirect
from django.contrib.auth.hashers import  check_password
from django.views import  View
from store.models.product import  Product
from store.models.category import  Category
from store.models.brand import  Brand
from .forms import OrderForm,ViewCartForm,PaymentForm
from django.contrib.auth.decorators import login_required
from store.middlewares.auth import auth_middleware
import random

def lart(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')

    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)
    
    if not cart:
        request.session['cart'] = {}
        productes={}
        products={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
        products = Product.get_products_by_id(list(request.session.get('cart').keys()))

    return render(request , 'cart.html' , {'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'products':products,'productes' : productes,'brands':brands,'categories':categories} )



def details(request, id):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')

    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)

    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    form=ViewCartForm()
    if request.method=='POST':
        product = request.POST.get('product')
        cart = request.session.get('cart')
        quantitey = cart.get(product)
        form=ViewCartForm(request.POST)
        if form.is_valid():
            cart[product] = form.cleaned_data.get('quantity')
    product=Product.objects.get(id=id)
    related_products = list(Product.objects.filter(category=product.category.id).exclude(id=product.id))
    related_products=random.sample(related_products, len(related_products))
    k=random.randint(1, 25)
    G=random.randint(1, 20)

    context={'k':k,'G':G,'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'related_products': related_products,'product':product,'form':form,'productes':productes,'brands':brands,'categories':categories}
    cart = request.session.get('cart')

    request.session['cart'] = cart
    

    return render(request , 'viewproduct.html',context)

#@login_required(login_url='login')
def checkout1(request):
    cart = request.session.get('cart')

    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)


    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Brand.get_all_brand()
    brandID = request.GET.get('brand')
    form=PaymentForm()
    if request.method=='POST':
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        elif brandID:
            products = Product.get_all_products_by_brandid(brandID)
        paginator=Paginator(products,30)
        page_number=request.GET.get('page')
    
    

        print(page_number)
        product_list = paginator.get_page(page_number)
        return render(request , 'index.html',{'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'product_list' : product_list,'categories':categories,'brands':brands,'productes':productes})
    return render(request , 'checkout1.html',{'form':form,'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'checkout':'checkout','categories':categories,'brands':brands,'productes':productes})

def remove_to_cart(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('lart')

def remove_to_store(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('store')
    
def remove_to_checkout(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('checkout1')
def remove_to_homepage(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('homepage')
def remove_to_orders(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('orders')






