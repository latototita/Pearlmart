from django.db import models
from .category import Category
from .brand import Brand
import datetime
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    del_price= models.IntegerField(default=0)
    selling_price =models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    category =models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=1000,blank=True,null=True)
    #image =models.ImageField(upload_to='Uploads/products/', blank=False)
    image=CloudinaryField('image')
    shop=models.CharField(max_length=100,default=1)
    shop_name =models.CharField(max_length=100,default='Pearlmart',blank=True)
    dates= models.DateTimeField(default=timezone.now)
    discount=models.BooleanField(default=False)
    discount_percentage=models.IntegerField(default=0)
    is_featured=models.BooleanField(default=False)
    is_top_rated=models.BooleanField(default=False)
    is_best_selling=models.BooleanField(default=False)
    is_new_arrival=models.BooleanField(default=False)
    is_most_viewed=models.BooleanField(default=False)
    is_new_product=models.BooleanField(default=False)
    is_hot_sale=models.BooleanField(default=False)
    is_hot_deal=models.BooleanField(default=False)
    onauction=models.BooleanField(default=False)


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids).order_by('-id')


    @staticmethod
    def get_product_by_id(id):
        return Product.objects.filter(id__in =id).order_by('?')







    @staticmethod
    def get_all_products():
        return Product.objects.all().order_by('?')

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id).order_by('?')
        else:
            return Product.objects.all().order_by('?');


    @staticmethod
    def get_all_products_by_brandid(brand_id):
        if brand_id:
            return Product.objects.filter(brand = brand_id).order_by('?')
        else:
            return Product.objects.all().order_by('?');


    @staticmethod
    def get_all_product():
        return Product.objects.all().order_by('?')

    def __str__(self):
    
        return self.name
