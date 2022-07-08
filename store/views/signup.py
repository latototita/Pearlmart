from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .home import store
from django.views import View
from .forms import RegistrationForm
from store.models.product import Product


def signup(response):
    brands = Brand.get_all_brand()
    categories = Category.get_all_categories()
    if response.method=="POST":
        form=RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('store')
    else:
        form=RegistrationForm()

    return render(response,'signup.html',{'tagged_cat':tagged_cat,'fashion_cat':fashion_cat,'tech_cat':tech_cat,'cat_home':cat_home,'party_cat':party_cat,'form':form,'brands':brands,'categories':categories})