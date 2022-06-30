
from datetime import datetime


def daily_accounting(request):
    today = datetime.datetime.today()
    number_of_products=0
    number_of_orders=0
    number_of_customers=0
    Products_Sold=[]
    gross_income_selling=0
    gross_income_cost=0
    New_Orders=[]
    profits=0
    gross_income_transport=0
    if not Account.objects.filter(date_created=today).filter(status =True):
        '''print('pass : ')
    
        print('Failed try 1')
        todays_accounting=[]
        print('Failed try 1')
        pass
    try:
        todays_accounting= Accounts.objects.filter(date_created=today).filter(status =True)
    except Exception as e:
        raise e
    else:
        return HttpResponse('else')
    if todays_accounting==[]:'''
        if Order.objects.filter(date=today).filter(status =True):
            Orders_today=Order.objects.filter(date=today).filter(status =True)
            if Orders_today.first():
                print('Orders not Empty')
                for order in Orders_today:
                    if order.customer not in New_Orders:
                        New_Orders.append(order.customer)
                        number_of_orders=number_of_orders+1
                        number_of_customers=number_of_customers+1
                        gross_income_transport= gross_income_transport+3000
                    if order.product not in Products_Sold:
                        Products_Sold.append(order.product)
                    number_of_products=number_of_products+order.quantity
                    gross_income_selling=gross_income_selling+(order.price*order.quantity)
                    product=Product.objects.get(id=order.product.id)
                    gross_income_cost=gross_income_cost+(product.selling_price*order.quantity)
                    cost_price=(product.selling_price*order.quantity)
                    selling_price=(order.price*order.quantity)
                    print(product.selling_price)
                gross_income_selling=(gross_income_selling+gross_income_transport)
                print('gross_income_selling :',gross_income_selling)
                gross_profit=(gross_income_selling- gross_income_cost)
                print('gross_profit  :',gross_profit)
                profits=(selling_price-cost_price)+gross_income_transport
                if Credit.objects.filter(date=today):
                    Credit=Credit.objects.filter(date=today)
                    if Credit.first():
                        for credit in Credit:
                            profits=(profits+credit.amount)
                else:
                    pass
                if Expenses.objects.filter(date=today):
                    Expenses=Expenses.objects.filter(date=today)
                    if Expenses.first():
                        for expense in Expenses:
                            profits=(profits-expense.amount)
                    else:
                        pass
                else:
                    pass
                if Debt.objects.filter(date=today):
                    Debt=Debt.objects.filter(date=today)
                    if Debt.first():
                        for debt in Debt:
                            profits=(profits-debt.amount)
                    else:
                        pass
                else:
                    pass

                print('profits :', profits)
                for product in Products_Sold:
                    product=Product.objects.get(id=order.product.id)
                    products_Sold = Products_Sold(
                        name=product.name,
                        price=product.price,
                        category=product.category.name,
                        brand=product.brand.name,
                        shop=product.shop,
                        is_discounted=product.discount,
                        discount_percentage=product.discount_percentage,)
                    products_Sold.save()
                accounts = Account(
                    gross_income=gross_income_selling,
                    gross_profit=profits,
                    net_profit=profits,
                    number_of_products=number_of_products,
                    number_of_orders=number_of_orders)
                accounts.save()
                net_profits=Net_Profit(
                    amount=profits)
                net_profits.save()
        
            else:
                print('Empty No Order today')
                return HttpResponse('Empty No Order today')
        return HttpResponse('Empty')
    elif todays_accounting.first():
        print('todays_accounting handled already')
        return HttpResponse('todays_accounting handled already')


class Account(models.Model):
    gross_income = models.IntegerField(default=0)
    gross_profit = models.IntegerField(default=0)
    net_profit = models.IntegerField(default=1)
    date_created = models.DateTimeField(default=timezone.now)
    number_of_products =models.IntegerField(default=0)
    number_of_orders = models.CharField(max_length=50, default='', blank=True)
    
    




class Products_Sold(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    shop =models.CharField(max_length=100,default='Pearl',blank=True)
    date_sold= models.DateTimeField(default=timezone.now)
    is_discounted=models.BooleanField(default=False)
    discount_percentage=models.IntegerField(default=0)
    


class Net_Profit(models.Model):
    amount=models.IntegerField(default=0)
    date_created=models.DateTimeField(default=timezone.now)

class Expense(models.Model):
    amount= models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    date_created=models.DateTimeField(default=timezone.now)

class Credit(models.Model):
    amount= models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    is_paid=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=timezone.now)

class Debt(models.Model):
    amount= models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    is_paid=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=timezone.now)


class Asset(models.Model):
    Costs =models.IntegerField(default=0)
    reason=models.CharField(max_length=2000)
    date_created=models.DateTimeField(default=timezone.now)


