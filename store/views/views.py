from store.models.models import *
from store.models.brand import Brand
from store.models.category import Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from Eshop import settings
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
import random
from .login import Login
from django.contrib.auth.models import Group
from store.models.product import Product
from django.contrib.admin.views.decorators import staff_member_required

def group_check(user):
    return user.groups.filter(name__in=['Vendor'])

def  Contact1(request):
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
    context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'productes':productes,'brands':brands,'categories':categories}
    return render(request,'contactus.html',context)


def  Contact(request):
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
    subject = request.POST.get('contact_subject')
    message = request.POST.get('message')
    
    if request.method=='POST':
        if request.user.is_authenticated:
            message=f'{message}............repely to {request.user.email}'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = True,
                    )
            send_mail(subject,
                    f'Your message has been received successfully, we will get back to you has soon has we can!!!. Have a lovely day',
                    settings.EMAIL_HOST_USER,
                    [f'{request.user.email}'],
                    fail_silently = True,
                    )
            messages.success(request, f'We have received your message, You will receive and email confirming it soon, Have a lovely day')
            return redirect('store')
        else:
            message=f'{message}............'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = True,
                    )
            messages.success(request, f'We have received your message successfully.\n Please signup here pearlmart.ml/signup or login here pearlmart.ml/login so that we can always get back to you via your email.\n , You will recive and email confirming it soon, Have a lovely day')
            return redirect('store')
    else:
        messages.success(request, f'Ooops Due to a possible Error in Our system, Your message was not recived, Please Try again!!!.')
        context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'productes':productes,'brands':brands,'categories':categories}
        return render(request,'contactus.html',context)

def  Contact_Us1(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    context={'productes':productes,'brands':brands,'categories':categories}
    return render(request,'Contact_Us.html',context)


    
def  Contact_Us(request):
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
    subject = request.POST.get('contact_subject')
    message = request.POST.get('message')
    context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'productes':productes,'brands':brands,'categories':categories}
    if request.method=='POST':
        if request.user.is_authenticated:
            message=f'{message}............repely to {request.user.email}'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = True,
                    )
            send_mail(subject,
                    f'Your message has been received successfully, we will get back to you has soon has we can!!!. Have a lovely day',
                    settings.EMAIL_HOST_USER,
                    [f'{request.user.email}'],
                    fail_silently = True,
                    )
            messages.success(request, f'We have received your message, You will recive and email confirming it soon, Have a lovely day')
            return redirect('Dashboard')
        else:
            message=f'{message}............'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = True,
                    )
            messages.success(request, f'We have recived your message, You will recive and email confirming it soon, Have a lovely day')
            return redirect('Dashboard')
    else:
        messages.success(request, f'Ooops Due to a possible Error in Our system, Your message was not recived, Please Try again!!!.')
        return render(request,'Contact_Us.html',context)

@login_required(login_url='login')
def become_vendor1(request):
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
    try:
        user = Vendor.objects.get(vendor=request.user.id)
    except:
        user=None
    if user is None:
        context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'Become_Vendor':'Become_Vendor','brands':brands,'categories':categories,'productes':productes}
        messages.success(request, f'Sell On Our Site for free,Up to End of July,for those who register Before the month of April Ends')
        return render(request,'become_vendor.html',context)
    else:
        return redirect('Dashboard')


@login_required(login_url='login')
def become_vendor(request):
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
    phone=request.POST.get('phone')
    alternative_Phone=request.POST.get('alternative_Phone')
    location=request.POST.get('location')
    shop_name=request.POST.get('shop_name')
    user = request.user.id
    try:
        user = Vendor.objects.get(vendor=user)
    except:
        user=None
    if user is not None:
        return redirect('Dashboard')
    elif request.method=='POST':
        New_vendor=Vendor(
            phone=phone,
            alternative_Phone=alternative_Phone,
            location=location,
            shop_name=shop_name,
            vendor=request.user.id )
        try:
            new_group = Group.objects.get(name = 'Vendor')
        except:
            new_group_created= Group.objects.create(name='Vendor')
            new_group = Group.objects.get(name = 'Vendor')
        user=User.objects.get(id=request.user.id)
        user.groups.add(new_group)
        New_vendor.save()
        send_mail('New Vendor Joined',
            f'Your Have a new vendor, with the name of {request.user.username}, phone number : {phone}, Alternative Phone Number : {alternative_Phone}, Shop name : {shop_name}, Located at : {location}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = True,
            )
        send_mail('Joined As a Pearl-Mart Vendor',
            f'You have successfully become a Pearl-Mart Vendor, click the following link to manage your selling account pearlmart.ml/Dashboard',
            settings.EMAIL_HOST_USER,
            [f'{request.user.email}'],
            fail_silently = True,
            )
        messages.success(request, f'Succefully Become a Pearl-Mart Vendor, Kindly Explore and add Products, Thank You.')
        return redirect('Dashboard')
    else:
        context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'Become_Vendor':'Become_Vendor','brands':brands,'categories':categories,'productes':productes}
        return render(request,'become_vendor.html',context)

# Create your views here.


@user_passes_test(group_check,login_url='become_vendor1')
def Dashboard(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    user=request.user.id
    username=request.user.username
    try:
        payment=Payment.objects.get(vendor_name=request.user.id)
    except:
        payment=None
    try:
        vendor=Vendor.objects.get(vendor=request.user.id)
    except:
        vendor=None
    try:
        orders=Order.objects.get(shop=request.user.id)
    except:
        orders=None
    context={'vendor':vendor,'orders':orders,'payment':payment,'brands':brands,'categories':categories}
    return render(request,'VendorAccountdetails.html',context)


@user_passes_test(group_check)
def Payment_update(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    try:
        payment = Payment.objects.get(key=request.user.id)
    except:
        messages.success(request, f'You Have no payment option registered, Please register on this page')
        return redirect('payment')
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Dashboard')
    else:
        form = PaymentForm(instance=payment)
        context={'form': form,'names':'Payment_update'}

    return render(request,'Change.html',context)


@user_passes_test(group_check)
def Product_update(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    product= Product.objects.get(id=id)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            feed_back=form.save(commit=False)
            l =[10,13,18,15,60,45,34,43,24,26,19,31,47,51,50,12,8,37,27]
            ld=random.sample(l, len(l))
            discount_percentage=ld[2]
            price=(((6/100)*form.cleaned_data['selling_price'])+form.cleaned_data['selling_price'])
            discounted_price=(((int(discount_percentage)/100)*price)+price)
            feed_back.del_price=discounted_price
            feed_back.price=price
            feed_back.shop=request.user.id
            feed_back.discount_percentage=discount_percentage
            Shop_name=Vendor.objects.get(vendor=request.user.id)
            feed_back.shop_name=Shop_name.shop_name
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('productboard')
    else:
        form = ProductUpdateForm(instance=product)
        context={'form': form,'products':'products','productes':productes,'product':product}

    return render(request,'add1.html',context)

@login_required
@user_passes_test(group_check)
def Vendor_update_get(request):
    vendor= Vendor.objects.get(vendor=request.user.id)
    form = AddVendor_UpdateForm(instance=vendor)
    context={'form': form,'vendor':'vendor','name':'Vendor','names':'Vendor_update'}
    return render(request,'Change.html',context)

@login_required
@user_passes_test(group_check)
def Vendor_update(request):
    
    vendor= Vendor.objects.get(vendor=request.user.id)
    if request.method == 'POST':
        form = AddVendor_UpdateForm(request.POST, instance=vendor)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Dashboard')
    form = AddVendor_UpdateForm(instance=vendor)
    context={'form': form,'vendor':'vendor','name':'Vendor','names':'Vendor_update'}
    messages.success(request, f'unsuccessful')
    return render(request,'Change.html',context)


@user_passes_test(group_check)
def Brand_add(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    if request.method == 'POST':
        form = AddBrandForm(request.POST, request.FILES)
        if form.is_valid():
            # update the existing `Band` in the database

            feedback=form.save(commit=False)
            feedback.shop=request.user.id
            feedback.save()
            # redirect to the detail page of the `Band` we just updated
            messages.success(request, f'Brand item : {form.cleaned_data["name"]}, Has Been Added Successfully')
            return redirect('Brand_add')

    else:
        brands=Brand.objects.filter(shop=request.user.id)
        form = AddBrandForm()
        messages.success(request, f'Add Or Customize Your Own brand')
        context={'form': form,'brands':brands,'brand':'brand','productes':productes,'name':'Brand','names':'Brand_add'}

    return render(request,'Change.html',context)


@user_passes_test(group_check)
def Category_add(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            # update the existing `Band` in the database
            feedback=form.save(commit=False)
            feedback.shop=request.user.id
            feedback.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Category_add')
    else:
        categories=Category.objects.filter(shop=request.user.id)
        form = AddCategoryForm()
        context={'form': form,'categories':categories,'category':'category','productes':productes,'name':'Category','names':'Category_add'}

    return render(request,'Change.html',context)

@user_passes_test(group_check)
def Brand_update(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    brand= Brand.objects.get(id=id)

    if request.method == 'POST':
        form = AddBrandForm(request.POST, instance=brand)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Brand_add')
    else:
        form = AddBrandForm(instance=brand)
        context={'form': form,'brand_updated':'brand_updated','updated':'updated','name':'Brand'}

    return render(request,'Change.html',context)
@user_passes_test(group_check)
def Category_update(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    category= Category.objects.get(id=id)

    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Category_add')
    else:
        form = AddCategoryForm(instance=category)
        
        context={'form': form,'category_updated':'category_updated','updated':'updated','name':'Category'}

    return render(request,'Change.html',context)

@user_passes_test(group_check)
def Product_delete(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    product=Product.objects.get(id=id)
    produc=Product.objects.get(id=id).delete()
    messages.success(request, f'Product item : {product.name}, Has Been deleted Successfully')
    return redirect('productboard')



@user_passes_test(group_check)
def Category_delete(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    category=Category.objects.get(id=id)
    categorys=Category.objects.get(id=id).delete()

    messages.success(request, f'Category item : {category.name}, Has Been deleted Successfully')
    return redirect('Category_add')
@user_passes_test(group_check)
def Brand_delete(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    brand=Brand.objects.get(id=id)
    brands=Brand.objects.get(id=id).delete()

    messages.success(request, f'Brand item : {brand.name}, Has Been deleted Successfully')
    return redirect('Brand_add')

@user_passes_test(group_check)
def productboard(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    products=Product.objects.filter(shop =request.user.id)

    context={'products':products}
    return render(request,'VendorProducts.html',context)


@user_passes_test(group_check)
def payment(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            # update the existing `Band` in the database
            feedback=form.save(commit=False)
            feedback.key=request.user.id
            vendor_name=Vendor.objects.get(vendor=request.user.id)
            feedback.vendor_name=vendor_name.shop_name
            feedback.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Dashboard')
    else:
        categories=Category.objects.filter(shop=request.user.id)
        form = PaymentForm()
        return render(request, 'payment.html', {'form' : form})
'''
@user_passes_test(group_check)
def Payment(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    user = request.user.id
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
  
        if form.is_valid():
            feedback=form.save(commit=False)
            feedback.name=request.user.id
            feedback.vendor_name=request.user.id
            feedback.save()

            return redirect('Dashboard')
    form = PaymentForm()
    return render(request, 'payment.html', {'form' : form})

'''
# Create your views here.
@user_passes_test(group_check)
def vendor_add_product(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    user = request.user.id
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            feed_back=form.save(commit=False)
            l =[10,13,18,15,60,45,34,43,24,26,19,31,47,51,50,12,8,37,27]
            ld=random.sample(l, len(l))
            discount_percentage=ld[2]
            price=(((10/100)*form.cleaned_data['selling_price'])+form.cleaned_data['selling_price'])
            price=round(price, -2)
            discounted_price=(((int(discount_percentage)/100)*price)+price)
            feed_back.del_price=discounted_price
            feed_back.price=price
            feed_back.shop=request.user.id
            feed_back.discount_percentage=discount_percentage
            Shop_name=Vendor.objects.get(vendor=request.user.id)
            feed_back.shop_name=Shop_name.shop_name
            feed_back.save()
            return redirect('view_admin')
    else:
        form = AddProductForm()
    return render(request, 'add1.html', {'form' : form})


@user_passes_test(group_check)
def view_admin(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    product_list=Product.objects.filter(shop=request.user.id)
    context={'product_list':product_list}
    return render(request,'Vadmin.html', context)

@user_passes_test(group_check)
def Vdeleteproduct(request,id):
    product=Product.objects.get(id=id).delete()
    return redirect('productboard')

@user_passes_test(group_check)
def stopvending(request):
    customer = request.session.get('customer')
    user=request.user.id
    products=Product.objects.get(shop=customer).delete()
    group = Group.objects.get(name='Vendor') 
    user.groups.remove(group)
    vendor=Vendor.objects.get(vendor=customer).delete()
    orders=Order.objects.get(shop=user).delete()

    return redirect('store')

@user_passes_test(group_check)
def vdetail(request, id):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    user= request.user.id
    categories = Category.get_all_categories()
    brands = Brand.get_all_brand()
    product=Product.objects.get(id=id)
    Others=list(Product.objects.filter(shop=user).exclude(id=product.id))

    context={'product':product,'Others':Others}
    return render(request , 'Vviewproduct.html',context)

@user_passes_test(group_check)
def VendorOrders(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    user= request.session.get('customer')
    orders=Order.objects.filter(shop=user)




















# HTTP Error 400
def bad_request(request, exception):
    response = render(
        '400.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 400
    send_mail('Error',
            f'400,bad_request error page. Attend to this immediately,here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = True,
            )

    return response

# HTTP Error 500
def server_error(request):
	context = {}
	response = render(request, "500.html", context=context)
	response.status_code = 500
	send_mail('Error',
            f'500,server_error error page. Attend to this immediately, here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = True,
            )
	return response

# HTTP Error 404
def page_not_found(request, exception):
    response = render(
        '404.html',
        context_instance=RequestContext(request)
        )
    
    response.status_code = 404
    send_mail('Error',
            f'404,page_not_found error page. Attend to this immediately, here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = True,
            )

    return response

# HTTP Error 403
def permission_denied(request, exception):
    response = render(
        '403.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 403
    send_mail('Erro',
            f'403,permission_denied error page. Attend to this immediately, here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = True,
            )
    return response

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 20


    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post 
    template_name = 'blog/post_detail.html'
    context_object_name='posts'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name='blog'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    context_object_name='blog'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    context_object_name='blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def About(request):
    posts=Post.objects.all().order_by('-id')[:3]
    return render(request, 'About_us.html', {'posts':posts})


@login_required(login_url='login')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('index')
    return redirect('post_detail', pk=pk)

@staff_member_required
def daily_accounting(request):
    today = datetime.datetime.today()
    number_of_products=0
    number_of_orders=0
    number_of_customers=0
    Product_Sold=[]
    gross_income_selling=0
    gross_income_cost=0
    New_Orders=[]
    profits=0
    gross_income_transport=0
    if Order.objects.filter(dates=today).filter(status=True).filter(is_accounted=False):
        Orders_today=Order.objects.filter(dates=today).filter(status =True)
        if Orders_today.first():
            for order in Orders_today:
                if order.customer not in New_Orders:
                    New_Orders.append(order.customer)
                    number_of_orders=number_of_orders+1
                    number_of_customers=number_of_customers+1
                    gross_income_transport= gross_income_transport+3000
                if order.product not in Product_Sold:
                    Product_Sold.append(order.product)
                number_of_products=number_of_products+order.quantity
                gross_income_selling=gross_income_selling+(order.price*order.quantity)
                product=Product.objects.get(id=order.product.id)
                gross_income_cost=gross_income_cost+(product.selling_price*order.quantity)
                cost_price=(product.selling_price*order.quantity)
                selling_price=(order.price*order.quantity)
                print(product.selling_price)
                orders=Order.objects.get(id=order.id)
                orders.is_accounted=True
                orders.save()
            gross_income_selling=(gross_income_selling+gross_income_transport)
            gross_profit=(gross_income_selling- gross_income_cost)
            profits=(selling_price-cost_price)+gross_income_transport
            if Credit.objects.filter(date_created=today):
                Credits=Credit.objects.filter(date_created=today)
                if Credit.first():
                    for credit in Credits:
                        profits=(profits+credit.amount)
            else:
                pass
            if Expense.objects.filter(date_created=today):
                Expenses=Expenses.objects.filter(date_created=today)
                if Expenses.first():
                    for expense in Expenses:
                        profits=(profits-expense.amount)
                else:
                    pass
            else:
                pass
            if Debit.objects.filter(date_created=today):
                Debt=Debit.objects.filter(date_created=today)
                if Debt.first():
                    for debt in Debt:
                        profits=(profits-debt.amount)
                else:
                    pass
            else:
                pass

            for product in Product_Sold:
                if Products_Sold.objects.filter(dates=today):
                    if Products_Sold.objects.filter(date_sold=today).filter(name=product.name):
                        pass
                    else:
                        product=Product.objects.get(id=order.product.id)
                        products_Sold = Products_Sold(
                            name=product.name,
                            price=product.price,
                            category=product.category.name,
                            brand=product.brand.name,
                            shop=product.shop,
                            is_discounted=product.discount,
                            discount_percentage=product.discount_percentage,)
                        products_Sold.save()
            if Account.objects.filter(date_created=today):
                Account_today=Account.objects.filter(date_created=today)
                Account_today.gross_income=(gross_income_selling+Account_today.gross_income)
                Account_today.gross_profit=(gross_profit+Account_today.gross_profit)
                Account_today.net_profits=(profits+Account_today.net_profits)
                Account_today.number_of_products=(number_of_products+Account_today.number_of_products)
                Account_today.number_of_orders=(number_of_orders+Account_today.number_of_orders)
                Account_today.number_of_customers=(number_of_orders+Account_today.number_of_customers)
                Account_today.save()
            else:
                accounts = Account(
                    gross_income=gross_income_selling,
                    gross_profit=gross_profit,
                    net_profit=profits,
                    number_of_products=number_of_products,
                    number_of_orders=number_of_orders)
                accounts.save()
            if Net_Profit.objects.filter(date_created=today):
                Net_pros=Net_Profit.objects.filter(date_created=today)
                Net_pros.amount=(Net_pros.amount+profits)
                Net_pros.save()
            else:
                net_profits=Net_Profit(
                    amount=profits)
                net_profits.save()
        return HttpResponse('Done')
    
    else:
        print('Not Done')
        return HttpResponse('Empty No Order today')



