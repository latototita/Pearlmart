from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.http import JsonResponse
from django.urls import path
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from store.models.models import *
from store.models.product import Product
from store.models.orders import Order
from store.models.category import Category
from store.models.brand import Brand



class Products_Sold_graph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        Products=Products_Sold.objects.all()
        date=[]
        for i in Products:
            date.append(i.id)
        return date

    def get_providers(self):
        """Return names of datasets."""
        return ["Selling Price", "Cost Price",]

    def get_data(self):
        """Return 3 datasets to plot."""
        Products=Products_Sold.objects.all()
        selling_price=[]
        cost_price=[]
        for i in Products:
            selling_price.append(i.price)
            cost_price.append(i.selling_price)


        return [selling_price,cost_price]
line_chart_json_products_sold = Products_Sold_graph.as_view()


class Netprofitgraph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        profits=Net_Profit.objects.all()
        Profit=[]
        for profit in profits:
            Profit.append(profit.date_created)
        return Profit

    def get_providers(self):
        """Return names of datasets."""
        return ["Selling Price", "Cost Price",]

    def get_data(self):
        """Return 3 datasets to plot."""
        amount=Net_Profit.objects.all()
        Amount=[]
        for a in amount:
            Amount.append(a.date_created)
        return Amount

line_chart_json_net_profit = Netprofitgraph.as_view()

class Creditgraph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        Credits=Credit.objects.all()
        date=[]
        for i in Credits:
            date.append(i.date_created)
        return date

    def get_providers(self):
        """Return names of datasets."""
        return ["Amount You Lent Out"]

    def get_data(self):
        """Return 3 datasets to plot."""
        Credits=Credit.objects.all()
        now=[]
        for i in Credits:
            now.append(i.amount)

        return now
line_chart_json_credit = Creditgraph.as_view()


class Debitgraph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        Debits=Debit.objects.all()
        date=[]
        for i in Debits:
            date.append(i.date_created)
        return date

    def get_providers(self):
        """Return names of datasets."""
        return ["Amount You Borrowed"]

    def get_data(self):
        """Return 3 datasets to plot."""
        Debits=Debit.objects.all()
        now=[]
        for i in Debits:
            now.append(i.amount)

        return now
line_chart_json_debit = Debitgraph.as_view()

class Assetgraph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        Assets=Asset.objects.all()
        date=[]
        for i in Assets:
            date.append(i.date_created)
        return date

    def get_providers(self):
        """Return names of datasets."""
        return ["Amount You Borrowed"]

    def get_data(self):
        """Return 3 datasets to plot."""
        Assets=Asset.objects.all()
        now=[]
        for i in Assets:
            now.append(i.costs)

        return [now]
line_chart_json_asset = Assetgraph.as_view()



class Expensegraph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        Expenses=Expense.objects.all()
        date=[]
        for i in Expenses:
            date.append(i.date_created)
        return date

    def get_providers(self):
        """Return names of datasets."""
        return ["Amount"]

    def get_data(self):
        """Return 3 datasets to plot."""
        Expenses=Expense.objects.all()
        amount=[]
        for i in Expenses:
            amount.append(i.amount)

        return amount
line_chart_json_expense = Expensegraph.as_view()



class Accountgraph(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        Accounts=Account.objects.all()
        date=[]
        for i in Accounts:
            date.append(i.date_created)
        return date

    def get_providers(self):
        """Return names of datasets."""
        return ["Gross Income","Gross Profit","Net Profit","Number of Orders","Number of Products","Number of Customers"]

    def get_data(self):
        """Return 3 datasets to plot."""
        Accounts=Account.objects.all()

        gross_income=[]
        gross_profit=[]
        net_profit=[]
        number_of_orders=[]
        number_of_products=[]
        number_of_customers=[]

        for i in Accounts:
            gross_income.append(i.gross_income)
            gross_profit.append(i.gross_profit)
            net_profit.append(i.net_profit)
            number_of_orders.append(i.number_of_orders)
            number_of_products.append(i.number_of_products)
            number_of_customers.append(i.number_of_customers)

        return gross_income,gross_profit,net_profit,number_of_orders,number_of_products,number_of_customers
line_chart_json_account = Accountgraph.as_view()
