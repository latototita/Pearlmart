from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Product
from store.models.models import *
from store.models.category import Category
from store.models.brand import Brand
from django.views import View
from store.models.orders import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    products = {}
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Brand.get_all_brand()
    brandID = request.GET.get('brand')
    results=request.GET.get("kw")
    k=request.GET.get('caution')
    customer = request.user.id
    if k:
        Order.objects.filter(id=k,customer=customer).delete()
        orders = Order.get_orders_by_customer(customer)
        messages.success(request, 'Order Item deleted Successfully')
        return render(request , 'orders.html'  , {'orders' : orders})
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    
        k=Category.objects.filter(id= categoryID)
    elif brandID:
        products = Product.get_all_products_by_brandid(brandID)
        k=brandID
    else:
        products = Product.get_all_products().order_by('-id');
        k=None
    random.shuffle(list(products))
    #paginator=Paginator(products,6)
    #page_number=request.GET.get('page')
      
    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)

    if request.user.is_authenticated:
        vendor_present=Vendor.objects.filter(vendor=request.user.id)
        vendor_present_here={}
    else:
        vendor_present_here=None

    #product_list = paginator.get_page(page_number)
        
    context={'vendor_present_here':vendor_present_here,'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'store':'store','productes':productes,'product_list':products,'k':k,'brands':brands,'categories':categories,'brands':brands}
    return render(request, 'index.html', context)
def search(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)
    if request.method=="POST":
        categories = Category.get_all_categories()
        brands = Brand.get_all_brand()
        searched=request.POST['searched']
        try:
            multiple_q=Q(Q(name__icontains=searched) | Q(description__icontains=searched))
            products=Product.objects.filter(multiple_q).order_by('-id')
            random.shuffle(list(products))
            paginator=Paginator(products,6)
            page_number=request.GET.get('page')
            product_list = paginator.get_page(page_number)
        except:
            product_list={}
        print('Yo')
        context={'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'store':'store','productes':productes,'product_list':product_list,'searched':searched,'page_number':page_number,'brands':brands,'categories':categories}

        return render(request,'index.html', context)

        

def homepage(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    products ={}
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Brand.get_all_brand()
    brandID = request.GET.get('brand')

    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    elif brandID:
        products = Product.get_all_products_by_brandid(brandID)

    else:
        products = Product.get_all_products();



    top_rated=Product.objects.filter(is_top_rated=True).order_by('-dates')[:12]
    featured=Product.objects.filter(is_featured=True).order_by('-dates')[:12]
    best_selling= Product.objects.filter(is_best_selling=True).order_by('-dates')[:12]
    new_arrival=Product.objects.filter(is_new_arrival=True).order_by('-dates')[:12]
    new_product=Product.objects.filter(is_new_product=True).order_by('-dates')[:12]
    hot_sale=Product.objects.filter(is_hot_sale=True).order_by('-dates')[:12]
    hot_deal=Product.objects.filter(is_hot_deal=True).order_by('-dates')[:12]
    trending=Product.objects.filter(is_most_viewed=True).order_by('-dates')[:12]

 
    random.shuffle(list(top_rated))
    random.shuffle(list(featured))
    random.shuffle(list(best_selling))
    random.shuffle(list(new_arrival))
    random.shuffle(list(new_product))
    random.shuffle(list(hot_sale))
    random.shuffle(list(hot_sale))
    random.shuffle(list(hot_deal))
    random.shuffle(list(products))

    latest=Post.objects.order_by('-date_posted')[:5]
    news=Post.objects.filter(is_news=True).order_by('-date_posted')[:3]

    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)



        
    context={'news':news,'latest':latest,'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'homepage':'homepage','trending':trending,'hot_deal':hot_deal,'productes':productes,'products':products,'brands':brands,'categories':categories ,'top_rated':top_rated,'featured':featured,'best_selling':best_selling,'new_arrival':new_arrival,'new_product':new_product,'hot_sale':hot_sale}

    return render(request, 'home.html', context)




def error_404_view(request, exception):
    return render(request,'404.html')
