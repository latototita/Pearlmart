from django.contrib.auth.models import User
from django.db import  models

class Brand(models.Model):
    name = models.CharField(max_length=20)
    shop =models.CharField(max_length=100,default='None',blank=True)
    is_popular=models.BooleanField(default=False)
    is_trending=models.BooleanField(default=False)
    is_tech=models.BooleanField(default=False)
    is_mobile=models.BooleanField(default=False)
    is_customized=models.BooleanField(default=False)
    is_ugandan=models.BooleanField(default=False)
    is_tagged=models.BooleanField(default=False)
    @staticmethod
    def get_all_brand():
        return Brand.objects.filter(product__isnull=False).distinct()


    def __str__(self):
        return self.name
