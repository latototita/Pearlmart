from store.models.models import *
from store.models.product import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
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

def auctionroom(request):
    auctions=Auction.objects.all()
    form=AuctionForm()
    if request.method=="POST":
        id= request.POST.get('item')
        auction=Auction.objects.get(id=id)
        form=AuctionForm(request.POST, instance=auction)
        if form.is_valid():
            feed_back=form.save(commit=False)
            feed_back.bidder=request.user
            feed_back.save()
            return redirect('auctionroom')
    return render(request, 'auction/index.html', {'auctions':auctions,'form':form})
