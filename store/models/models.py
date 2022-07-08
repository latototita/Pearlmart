from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import datetime
from .product import Product
from django.contrib.auth.models import User


class Vendor(models.Model):
    photo=models.ImageField(upload_to='profile', default='')
    phone=models.CharField(default='1',blank=True,max_length=10)
    location=models.CharField(default='',blank=True, max_length=100)
    alternative_Phone=models.CharField(default='1',blank=True,max_length=10)
    shop_name=models.CharField(default='',blank=True, max_length=100,unique=True)
    vendor=models.CharField(max_length=100,default='None',blank=True)
    dates = models.DateTimeField(default=datetime.datetime.today)


class Payment(models.Model):
    name=models.CharField(max_length=100,default='None',blank=True)
    mtn_name = models.CharField(max_length=100,default='None',blank=True)
    mtn=models.CharField(default='Empty',blank=True,max_length=10)
    airtel_name= models.CharField(max_length=100,default='None',blank=True)
    airtel=models.CharField(default='Empty',blank=True,max_length=10)
    wave_name= models.CharField(max_length=100,default='None',blank=True)
    wave=models.CharField(default='Empty',blank=True,max_length=10)
    vendor_name=models.CharField(max_length=100,default='None',blank=True)
    dates = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
    
        return self.vendor_name


class PostManager(models.Manager):
    def like_toggle(self, user, post_obj):
        if user in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(user)
        else:
            is_liked = True
            post_obj.liked.add(user)
        return is_liked


class Post(models.Model):
    image=models.ImageField(upload_to='posts')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    date_posted = models.DateTimeField(default=timezone.now)
    is_news=models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.author

class Account(models.Model):
    gross_income = models.IntegerField(default=0)
    gross_profit = models.IntegerField(default=0)
    net_profit = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=datetime.datetime.today)
    number_of_products =models.IntegerField(default=0)
    number_of_orders = models.IntegerField(default=0)
    number_of_customers = models.IntegerField(default=0)

class Products_Sold(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    shop =models.CharField(max_length=100,default='Pearl',blank=True)
    date_sold= models.DateTimeField(default=datetime.datetime.today)
    is_discounted=models.BooleanField(default=False)
    discount_percentage=models.IntegerField(default=0)
    def __str__(self):
    
        return self.name


class Net_Profit(models.Model):
    amount=models.IntegerField(default=0)
    date_created=models.DateTimeField(default=datetime.datetime.today)
    def __str__(self):
    
        return self.amount
class Expense(models.Model):
    amount= models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    date_created=models.DateTimeField(default=datetime.datetime.today)
    def __str__(self):
    
        return self.reason

class Credit(models.Model):
    amount= models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    is_paid=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=datetime.datetime.today)
    def __str__(self):
    
        return self.reason

class Debit(models.Model):
    amount= models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    is_paid=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=datetime.datetime.today)
    def __str__(self):
    
        return self.reason


class Asset (models.Model):
    costs =models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    date_created=models.DateTimeField(default=datetime.datetime.today)
    def __str__(self):
    
        return self.reason

class Order_record(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    selling_price =models.IntegerField(default=0)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date_created = models.DateField(default=datetime.datetime.today)
    email  = models.EmailField(max_length=70,blank=True,unique=False)
    status = models.BooleanField(default=False)
    ordering_code=models.CharField(max_length=6,default='')
    shop_name = models.CharField(max_length=50,default='')
    def __str__(self):
    
        return self.customer




