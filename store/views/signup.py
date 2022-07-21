from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .home import store
from .login import Login
from django.views import View
from .forms import RegistrationForm
from store.models.product import Product
from store.models.brand import Brand
from store.models.category import Category

def signup(response):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    fashion_cat=Category.objects.filter(is_tech=True)
    tech_cat=Category.objects.filter(is_fashion=True)
    cat_home=Category.objects.filter(is_home=True)
    party_cat=Category.objects.filter(is_party=True)
    tagged_cat=Category.objects.filter(is_tagged=True)
    
    if response.method=="POST":
        form=RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('Login')
    else:
        form=RegistrationForm()

    return render(response,'signup.html',{'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'form':form,'brands':brands,'categories':categories})