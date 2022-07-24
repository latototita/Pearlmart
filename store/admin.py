from django.contrib import admin
from store.models.models import *
from store.models.product import Product
from store.models.orders import Order
from store.models.category import Category
from store.models.brand import Brand
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display=('vendor','phone','location','alternative_Phone','shop_name','dates')
    search_fields = ('shop_name', 'location',)
    ordering=('-dates',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['Products'] = 'Products'
        extra_context['info'] = 'Number of Vendor Joining Per Day'
        # Aggregate new subscribers per day
        chart_data = (
            Vendor.objects.annotate(date=TruncDay("dates"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context['chart_data']= as_json   
        return super(VendorAdmin, self).changelist_view(request, extra_context=extra_context)

    
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted')
    list_display_links = ('id', 'title')
    list_filter = ('author', 'date_posted')
    search_fields = ('title', 'content', 'author')
    list_per_page = 20


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post',
                    'approved_comment', 'created_date')
    list_display_links = ('id', 'author', 'post')
    list_filter = ('author', 'created_date')
    list_editable = ('approved_comment', )
    search_fields = ('author', 'post')
    list_per_page = 20





class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price','stock','selling_price','category','brand','image','dates','shop_name','shop','discount','is_featured','is_top_rated','is_best_selling','is_new_arrival','is_most_viewed','is_new_product', 'is_hot_sale','is_hot_deal',]
    search_fields = ('name',)
    list_filter = ('brand', 'dates','category')
    ordering=('-dates',)
    list_editable = ('discount','selling_price','is_featured','shop_name','shop','is_top_rated','is_best_selling','is_new_arrival','is_most_viewed','is_new_product', 'is_hot_sale','is_hot_deal',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['Products'] = 'Products'
        extra_context['info'] = 'Number of Products Added Per Day'
        # Aggregate new subscribers per day
        chart_data = (
            Product.objects.annotate(date=TruncDay("dates"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context['chart_data']= as_json   
        return super(AdminProduct, self).changelist_view(request, extra_context=extra_context)



class AdminProducts_Sold(admin.ModelAdmin):
    list_display = ['name', 'price','category','brand','date_sold','is_discounted','discount_percentage']
    search_fields = ('name','category', 'brand','price')
    list_filter = ('brand', 'date_sold','category')
    ordering=('-date_sold',)
    list_editable = ('is_discounted',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Products_Sold'] = 'Products_Sold'
         extra_context['graph'] = 'graph'
         return super(AdminProducts_Sold, self).changelist_view(request, extra_context=extra_context)


class AdminNet_Profit(admin.ModelAdmin):
    list_display = ['amount','date_created']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Net_Profit'] = 'Net_Profit'
         extra_context['graph'] = 'graph'
         return super(AdminNet_Profit, self).changelist_view(request, extra_context=extra_context)

class AdminExpenses(admin.ModelAdmin):
    list_display = ['amount','date_created','reason']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Expense'] = 'Expense'
         extra_context['graph'] = 'graph'
         return super(AdminExpenses, self).changelist_view(request, extra_context=extra_context)


class AdminCredit(admin.ModelAdmin):
    list_display = ['amount','date_created','reason','is_paid']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Credit'] = 'Credit'
         extra_context['graph'] = 'graph'
         return super(AdminCredit, self).changelist_view(request, extra_context=extra_context)
    

class AdminAsset(admin.ModelAdmin):
    list_display = ['costs','date_created','reason']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Asset'] = 'Asset'
         extra_context['graph'] = 'graph'
         return super(AdminAsset, self).changelist_view(request, extra_context=extra_context)
    

class AdminOrder_record(admin.ModelAdmin):
    list_display = ['customer','product','price','quantity','address','phone','date_created','status','ordering_code']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['Products'] = 'Products'
        extra_context['graph'] = 'graph'
        extra_context['Order_Record'] = 'Order_Record'
        extra_context['info'] = 'Number of Products Ordered Per Day'
        # Aggregate new subscribers per day
        chart_data = (
            Order_record.objects.annotate(date=TruncDay("date_created"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context['chart_data']= as_json 
        return super(AdminOrder_record, self).changelist_view(request, extra_context=extra_context)
    

class AdminAccount(admin.ModelAdmin):
    list_display = ['gross_income','gross_profit','net_profit','date_created','number_of_orders','number_of_products']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Account'] = 'Account'
         extra_context['graph'] = 'graph'
         return super(AdminAccount, self).changelist_view(request, extra_context=extra_context)
    



class AdminDebit(admin.ModelAdmin):
    list_display = ['amount','date_created','reason','is_paid']
    ordering=('-date_created',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
         extra_context = extra_context or {}
         extra_context['Debit'] = 'Debit'
         extra_context['graph'] = 'graph'
         return super(AdminDebit, self).changelist_view(request, extra_context=extra_context)
    

class AdminBrand(admin.ModelAdmin):
    list_display = ['name']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminOrder(admin.ModelAdmin):
    list_display = ['customer','product','price','quantity','address','phone','dates','status','is_accounted','ordering_code']
    ordering=('-dates',)
    list_editable = ('status',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['Products'] = 'Products'
        extra_context['info'] = 'Number of Products Ordered Per Day'
        # Aggregate new subscribers per day
        chart_data = (
            Order.objects.annotate(date=TruncDay("dates"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context['chart_data']= as_json   
        return super(AdminOrder, self).changelist_view(request, extra_context=extra_context)


class AdminPayment(admin.ModelAdmin):
    list_display = ['key','dates','vendor_name']
    ordering=('-dates',)
    change_list_template = "../templates/change_list.html"
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['Products'] = 'Products'
        extra_context['info'] = 'Number of Payment Registration Per Day'
        # Aggregate new subscribers per day
        chart_data = (
            Payment.objects.annotate(date=TruncDay("dates"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context['chart_data']= as_json   
        return super(AdminPayment, self).changelist_view(request, extra_context=extra_context)



# Register your models here.
admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Order, AdminOrder )
admin.site.register(Brand,AdminBrand )
admin.site.register(Debit, AdminDebit)
admin.site.register(Products_Sold, AdminProducts_Sold)
admin.site.register(Account , AdminAccount)
admin.site.register(Asset, AdminAsset )
admin.site.register(Credit,AdminCredit)
admin.site.register(Payment,AdminPayment)
admin.site.register(Vendor, VendorAdmin)



admin.site.register(Expense, AdminExpenses)
admin.site.register(Order_record , AdminOrder_record)
admin.site.register(Net_Profit, AdminNet_Profit)
