from django.db import models
from .category import Category
from .brand import Brand
import datetime
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)
    category =models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=500, default='' , null=True , blank=True)
    image =models.ImageField(upload_to='Uploads/products/')
    shop =models.CharField(max_length=100,default='None',blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_featured=models.BooleanField(default=False)
    is_top_rated=models.BooleanField(default=False)
    is_best_selling=models.BooleanField(default=False)
    is_new_arrival=models.BooleanField(default=False)
    is_most_viewed=models.BooleanField(default=False)
    is_new_product=models.BooleanField(default=False)
    is_hot_sale=models.BooleanField(default=False)
    is_hot_deal=models.BooleanField(default=False)


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids).order_by('-id')


    @staticmethod
    def get_product_by_id(id):
        return Product.objects.filter(id__in =id).order_by('-id')







    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id).order_by('-id')
        else:
            return Product.get_all_products();


    @staticmethod
    def get_all_products_by_brandid(brand_id):
        if brand_id:
            return Product.objects.filter(brand = brand_id).order_by('-id')
        else:
            return Product.get_all_products();


    @staticmethod
    def get_all_product():
        return Product.objects.filter(order__isnull=False).distinct().order_by('-id')

    def __str__(self):
    
        return self.name
