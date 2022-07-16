from django.db import  models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=45)
    shop =models.CharField(max_length=100,default='None',blank=True)
    is_tech=models.BooleanField(default=False)
    is_fashion=models.BooleanField(default=False)
    is_home=models.BooleanField(default=False)
    is_party=models.BooleanField(default=False)
    is_tagged=models.BooleanField(default=False)
    @staticmethod
    def get_all_categories():
        return Category.objects.filter(product__isnull=False).distinct()


    def __str__(self):
        return self.name
