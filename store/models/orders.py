from django.db import models
from .product import Product
from .models import Method
from django.contrib.auth.models import User
import datetime


class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    selling_price =models.IntegerField(default=0)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    dates = models.DateField(default=datetime.datetime.today)
    email  = models.EmailField(max_length=70,blank=True,unique=False)
    status = models.BooleanField(default=False)
    ordering_code=models.CharField(max_length=60,default='')
    shop_name = models.CharField(max_length=60,default='Pearlmart')
    payment_method = models.ForeignKey(Method,
                                 on_delete=models.CASCADE)
    payment_verified = models.BooleanField(default=False)
    is_accounted = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()



    @staticmethod
    def get_by_id(id):
        if category_id:
            return Order.objects.filter(id=id).order_by('?')
        else:
            return None




    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-dates')


