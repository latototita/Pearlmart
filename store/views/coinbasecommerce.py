import logging

from coinbase_commerce.client import Client
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from store.models.models import *
from store.models.brand import Brand
from store.models.category import Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from Eshop import settings
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
import random
from .login import Login
from django.contrib.auth.models import Group
from store.models.product import Product
from django.contrib.admin.views.decorators import staff_member_required

def home_view(request):
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = 'http://localhost:8000/'
    ordering_code = request.session.get('ordering_code')
    total_price = request.session.get('total_price')
    dates = request.session.get('dates')
    customer = request.session.get('customer')
    if not ordering_code:
        return redirect('checkout1')
    total_price=str(total_price)
    ordering_code=str(ordering_code)
    dates=str(dates)
    customer=str(customer)
    product = {
        'name': 'Pearl-Mart',
        'description': 'Cryptocurrency Payment.',
        'local_price': {
            'amount': json.loads(total_price),
            'currency': 'UGX'
        },
        'pricing_type': 'fixed_price',
        'redirect_url': domain_url + 'success/',
        'cancel_url': domain_url + 'cancel/',
        'metadata': {
            'total_price':total_price,
            'ordering_code':ordering_code,
            'dates':dates,
            'customer':customer,
        },
    }
    charge = client.charge.create(**product)
    request.session['ordering_code']=''
    request.session['total_price']=''
    request.session['dates']=''
    request.session['customer']=''
    return render(request, 'home.html', {
        'charge': charge,
    })

def success_view(request):
    return redirect('index')


def cancel_view(request):
    return redirect('index')


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks

        if event['type'] == 'charge:confirmed':
            logger.info('Payment confirmed.')
            customer = event['data']['metadata']['customer']
            total_price = event['data']['metadata']['total_price']
            dates = event['data']['metadata']['dates']
            ordering_code = event['data']['metadata']['ordering_code']
            orders=Order.objects.filter(ordering_code=ordering_code)
            for order in orders:
                if order.customer==customer and order.dates==dates:
                    order.payment_verified=True
                    order.save()
            # TODO: run some custom code here
            # you can also use 'customer_id' or 'customer_username'
            # to fetch an actual Django user

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)