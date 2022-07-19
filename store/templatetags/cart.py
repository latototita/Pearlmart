from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;

 
@register.filter(name='cart_quantity')
def cart_quantity(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;


@register.filter(name='price_total')
def price_total(product  , cart):
    return int(product.price) * cart_quantity(product , cart)

@register.filter(name='total_cart_price')
def total_cart_price(productes , cart):
    sum = 0 ;
    for p in productes:
        sum += price_total(p , cart)
    return sum

@register.filter(name='total_cart_price_grand')
def total_cart_price_grand(productes , cart):
    sum = 0 ;
    for p in productes:
        sum += price_total(p , cart)
    sum=sum+3000
    return sum
    