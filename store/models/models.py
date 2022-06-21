from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import datetime
from django.contrib.auth.models import User


class Vendor(models.Model):
    phone=models.CharField(default='1',blank=True,max_length=10)
    location=models.CharField(default='',blank=True, max_length=100)
    alternative_Phone=models.IntegerField(default='1',blank=True)
    shop_name=models.CharField(default='',blank=True, max_length=100,unique=True)
    vendor=models.CharField(max_length=100,default='None',blank=True)


class Payment(models.Model):
    name=models.CharField(max_length=100,default='None',blank=True)
    mtn_name = models.CharField(max_length=100,default='None',blank=True)
    mtn=models.CharField(default='Empty',blank=True,max_length=10)
    airtel_name= models.CharField(max_length=100,default='None',blank=True)
    airtel=models.CharField(default='Empty',blank=True,max_length=10)
    wave_name= models.CharField(max_length=100,default='None',blank=True)
    wave=models.CharField(default='Empty',blank=True,max_length=10)
    vendor_name=models.CharField(max_length=100,default='None',blank=True)

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
