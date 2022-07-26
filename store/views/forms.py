from django.forms import ModelForm
from store.models.orders import Order
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models.product import Product
from store.models.brand import Brand
from store.models.category import Category
from django import forms
from store.models.models import *

class OrderForm(ModelForm):
	class Meta:
		model=Order
		fields=('address','phone')

class ViewCartForm(forms.ModelForm):
	class Meta:
		model=Order
		fields=('quantity','id',)
	def __init__(self, *args, **kwargs,):
		super().__init__(*args, **kwargs)
		self.fields['quantity']=forms.FloatField(max_value=1000, min_value=1)

'''
def __init__(self, min_value=None, *args, **kwargs):
		super(ViewCartForm, self).__init__(*args, **kwargs)
		self.fields['quantity'] = forms.IntegerField(min_value=1)'''
'''def __init__(self, *args, **kwargs,):
		super().__init__(*args, **kwargs)
		self.fields['quantity']=forms.IntegerField(max_value=1000, min_value=1)
		'''
class RegistrationForm(UserCreationForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=["username","email","password1","password2"]


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"




class PostForm(BaseForm):
    class Meta:
        model = Post
        fields = ['title','image','content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
    image=forms.ImageField(required=True)
# Your forms
class AddVendor_UpdateForm(BaseForm):
    class Meta:
        model = Vendor
        fields=('photo','phone','alternative_Phone','location','shop_name')
    photo= forms.ImageField(label='Edit Profile Photo')

class AddVendorForm(BaseForm):
    class Meta:
        required_fields = ['photo','phone','alternative_Phone','location','shop_name']
        model = Vendor
        fields=('photo','phone','alternative_Phone','location','shop_name')
    photo= forms.ImageField(label='Add Profile Photo',required=True)


    phone = forms.IntegerField(required=True)
    alternative_Phone = forms.IntegerField(required=True)
    location=forms.CharField(required=True)
    shop_name=forms.CharField(required=True)

class AddProductForm(BaseForm):
	class Meta:
		model=Product
		fields=('name','stock','brand',  'selling_price','image','description','category')
	name = forms.CharField(required=True)
	stock = forms.IntegerField(required=True)
	selling_price=forms.IntegerField(required=True)
	image=forms.ImageField(required=True)
class ProductUpdateForm(BaseForm):
	class Meta:
		model=Product
		fields=('name','stock','brand',  'selling_price','image','description','category')


class PaymentForm(ModelForm):
	class Meta:
		model=Payment
		fields=('mtn_name','mtn','airtel_name', 'airtel','wave_name','wave')
	mtn_name= forms.CharField(label='MTN Account Registration Name',required=False)
	airtel_name= forms.CharField(label='Airtel Account Registration Name',required=False)
	wave_name= forms.CharField(label='Wave Account Registration Name',required=False)

class AddBrandForm(ModelForm):
	class Meta:
		model=Brand
		fields=('name',)
	name= forms.CharField(label='Customize Your Own Brand for Products',required=True)

class AddCategoryForm(ModelForm):
	class Meta:
		model=Category
		fields=('name',)
	name= forms.CharField(label='Customize Your Own Category for Products',required=True)


