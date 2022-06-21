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
from django.core.mail import send_mail
from django.shortcuts import (
render_to_response
)
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test

from .login import Login
from django.contrib.auth.models import Group
from store.models.product import Product


def group_check(user):
    return user.groups.filter(name__in=['Vendor'])


def  Contact1(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    context={'productes':productes,'brands':brands,'categories':categories}
    return render(request,'contactus.html',context)


def  Contact(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    subject = request.POST.get('contact_subject')
    message = request.POST.get('message')
    
    if request.method=='POST':
        if user.is_authenticated:
            message=f'{message}............repely to {request.user.email}'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = False,
                    )
            send_mail(subject,
                    f'Your message has been recived successfully, we will get back to you has soon has we can!!!. Have a lovely day',
                    settings.EMAIL_HOST_USER,
                    [f'{request.user.email}'],
                    fail_silently = False,
                    )
            messages.success(request, f'We have recived your message, You will recive and email confirming it soon, Have a lovely day')
            return redirect('Contact_Us')
        else:
            message=f'{message}............'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = False,
                    )
            messages.success(request, f'We have recived your message, You will recive and email confirming it soon, Have a lovely day')
    else:
        messages.success(request, f'Ooops Due to a possible Error in Our system, Your message was not recived, Please Try again!!!.')
        context={'productes':productes,'brands':brands,'categories':categories}
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
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    subject = request.POST.get('contact_subject')
    message = request.POST.get('message')
    
    if request.method=='POST':
        if user.is_authenticated:
            message=f'{message}............repely to {request.user.email}'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = False,
                    )
            send_mail(subject,
                    f'Your message has been recived successfully, we will get back to you has soon has we can!!!. Have a lovely day',
                    settings.EMAIL_HOST_USER,
                    [f'{request.user.email}'],
                    fail_silently = False,
                    )
            messages.success(request, f'We have recived your message, You will recive and email confirming it soon, Have a lovely day')
            return redirect('Contact_Us')
        else:
            message=f'{message}............'
            send_mail(subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['pearlmartbusinesses@gmail.com'],
                    fail_silently = False,
                    )
            messages.success(request, f'We have recived your message, You will recive and email confirming it soon, Have a lovely day')
    else:
        messages.success(request, f'Ooops Due to a possible Error in Our system, Your message was not recived, Please Try again!!!.')
        context={'productes':productes,'brands':brands,'categories':categories}
        return render(request,'Contact_Us.html',context)

@login_required(login_url='login')
def become_vendor1(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
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
        context={'Become_Vendor':'Become_Vendor','brands':brands,'categories':categories,'productes':productes}
        messages.success(request, f'Sell On Our Site for free,Up to End of July,for those who register Before the month of April Ends')
        return render(request,'become_vendor.html',context)
    else:
        return redirect('Dashboard')


@login_required(login_url='login')
def become_vendor(request):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    cart = request.session.get('cart')
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
            ['pearlmartbusinesses@gmail.com',f'{request.user.email}'],
            fail_silently = False,
            )
        send_mail('New Vendor Joined',
            f'You have successfully become a Pearl-Mart Vendor, click the following link to manage your selling account pearlmart.ml/Dashboard',
            settings.EMAIL_HOST_USER,
            [f'{request.user.email}'],
            fail_silently = False,
            )
        messages.success(request, f'Succefully Become a Pearl-Mart Vendor, Kindly Explore and add Products, Thank You.')
        return redirect('Dashboard')
    else:
        context={'Become_Vendor':'Become_Vendor','brands':brands,'categories':categories,'productes':productes}
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
    payment = Payment.objects.get(name=request.user.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Dashboard')
    else:
        form = PaymentForm(instance=payment)
        context={'form': form}

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
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('productboard')
    else:
        form = AddProductForm(instance=product)
        context={'form': form,'products':'products','productes':productes,'product':product}

    return render(request,'add1.html',context)


@user_passes_test(group_check)
def Vendor_update(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    vendor= Vendor.objects.get(vendor=request.user.id)

    if request.method == 'POST':
        form = AddVendorForm(request.POST, instance=vendor)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('Dashboard')
    form = AddVendorForm(instance=vendor)
    context={'form': form,'vendor':'vendor','productes':productes,'name':'Vendor'}

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
        context={'form': form,'brands':brands,'brand':'brand','productes':productes,'name':'Brand'}

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
        context={'form': form,'categories':categories,'category':'category','productes':productes,'name':'Category'}

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
        context={'form': form,'name':'Brand'}

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
        
        context={'form': form,'name':'Category'}

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
    user = request.user.id
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
  
        if form.is_valid():
            feedback=form.save(commit=False)
            feedback.name=request.user.id
            feedback.vendor_name=request.user.id
            feedback.save()

            return redirect('Dashboard')
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form' : form})


# Create your views here.
@user_passes_test(group_check)
def vendor_add_product(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    user = request.session.get('customer')
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
  
        if form.is_valid():
            feed_back=form.save(commit=False)
            feed_back.shop=request.user.id
            feed_back.save()
            return redirect('view_admin')
    else:
        form = AddProductForm()
    return render(request, 'add1.html', {'form' : form})

'''def vendor_add_product(request):
    user = request.session.get('customer')
    if request.method=='POST':
        product=Product()
        name = request.POST.get("name")
        stock = request.POST.get("stock")
        price= request.POST.get("price")
        image =  request.POST['image']
        description = request.POST.get("description")
        brand = request.POST.get("brand")
        category = request.POST.get("category")
        brand=Brand.objects.get(id=brand)
        category=Category.objects.get(id=category)
        print(stock)
        print(price)
        product=Product(
            name=name,
            price=int(price),
            stock=int(stock),
            image=image,
            description=description,
            brand=brand,
            category=category,
            )
        product.shop=user
        product.save()
        print('laban')
        print(category)
        print(brand)
        product_list=Product.objects.filter(shop=user)
        context={'product_list':product_list}
        return redirect('view_admin')


        print('9')
    user= request.session.get('customer')
    brands=Brand.objects.all()
    categories=Category.objects.all()
    form=AddProductForm()
    print('10')
    context={'form':form,'addproduct':'addproduct','productes':productes','brands':brands,'categories':categories}
    return render(request,'add.html',context)
'''
@user_passes_test(group_check)
def view_admin(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    customer = request.session.get('customer')
    product_list=Product.objects.filter(shop=customer)
    context={'product_list':product_list}
    return render(request,'Vadmin.html', context)

@user_passes_test(group_check)
def Vdeleteproduct(request,id):
    product=Product.objects.get(id=id).delete()
    return redirect('Vadmin')

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
    response = render_to_response(
        '400.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 400
    send_mail('Error',
            f'400,bad_request error page. Attend to this immediately,here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = False,
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
            fail_silently = False,
            )
	return response

# HTTP Error 404
def page_not_found(request, exception):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request)
        )
    
    response.status_code = 404
    send_mail('Error',
            f'404,page_not_found error page. Attend to this immediately, here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = False,
            )

    return response

# HTTP Error 403
def permission_denied(request, exception):
    response = render_to_response(
        '403.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 403
    send_mail('Erro',
            f'403,permission_denied error page. Attend to this immediately, here {request.user.email}',
            settings.EMAIL_HOST_USER,
            ['pearlmartbusinesses@gmail.com'],
            fail_silently = False,
            )
    return response

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5


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
