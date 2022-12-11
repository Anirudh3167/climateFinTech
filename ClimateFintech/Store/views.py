from django.shortcuts import render, redirect
from Backend.models import Products,CartItems
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests
import random
# Create your views here.

def Home(request):
    return render(request,'storeHome.html')

def About(request):
    return render(request,'about_climate.html')

def ProductDetails(request,search):
    if request.method == 'GET':
        search = search.split('-')
        search1 = ''
        for i in search:    search1 = search1+' '+i
        print("SEARCH1:",search1)
        result = Products.objects.filter(Product_Name = search1[1:]).first()
        if result:
            context = model_to_dict(result)
        else:
            context = {}
            return redirect('store:home')
        return render(request,'storePrductDetails.html',context)
    elif request.method == 'POST':
        qty = request.POST['qty']
        code = request.POST['prod_code']
        check = CartItems.objects.filter(code = code).first()
        if check:
            prev_qty = check.qty
            update_cart_item = CartItems.objects.update(qty = str(int(prev_qty) + int(qty)))
        else:
            code = Products.objects.get(id = code)
            owner = request.user
            new_cart_item = CartItems.objects.create(owner=owner,qty=qty,code=code)
            new_cart_item.save()
        return redirect('store:cart')


@login_required(login_url='Login')
def Cart(request):
    user = request.user
    cart_items = CartItems.objects.filter(owner=user)
    context = {}
    count = 0
    sub_total = 0
    for i in cart_items:
        context[count] = model_to_dict(i)
        qty = context[count]['qty']
        product = model_to_dict(Products.objects.get(id = context[count]["code"]))
        price = product['Product_price']
        context[count]['multiply_res'] = str((float(price))*(float(qty)))[:8]
        sub_total = sub_total + (float(price))*(float(qty))
        for j in product:
            context[count][j] = product[j]
        count = count + 1
    if sub_total != 0:
        shipping = 4.99
        tax = 9.99
    else:
        shipping = 0
        tax = 0
    wrap = {}
    wrap['context'] = context
    wrap['sub_total'] = str(sub_total)[:8]
    wrap['shipping'] = shipping
    wrap['tax'] = tax
    wrap['total_amount'] = str(sub_total + shipping + tax)[:7]
    # print(wrap)
    return render(request,'storeCart.html',wrap)

@login_required(login_url='Login')
def RemoveCart(request,id):
    CartItems.objects.get(code=id).delete()
    print("Item Deleted")
    return redirect('store:cart')
####################################################
# RAPYD API RELATED
####################################################
#Utilities
base_url = 'https://sandboxapi.rapyd.net'
secret_key = '1937e64f424076550235f1c171e0027dc11dbe251eefceec727b74175919d2e0e7f01a4e8c3a99e9'
access_key = 'C34D595194D00BDA50F5'

def generate_salt(length=12):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def get_unix_time(days=0, hours=0, minutes=0, seconds=0):
    return int(time.time())

def update_timestamp_salt_sig(http_method, path, body):
    if path.startswith('http'):
        path = path[path.find(f'/v1'):]
    salt = generate_salt()
    timestamp = get_unix_time()
    to_sign = (http_method, path, salt, str(timestamp), access_key, secret_key, body)
    
    h = hmac.new(secret_key.encode('utf-8'), ''.join(to_sign).encode('utf-8'), hashlib.sha256)
    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))
    return salt, timestamp, signature

def current_sig_headers(salt, timestamp, signature):
    sig_headers = {'access_key': access_key,
                   'salt': salt,
                   'timestamp': str(timestamp),
                   'signature': signature,
                   'idempotency': str(get_unix_time()) + salt}
    return sig_headers

def pre_call(http_method, path, body=None):
    str_body = json.dumps(body, separators=(',', ':'), ensure_ascii=False) if body else ''
    salt, timestamp, signature = update_timestamp_salt_sig(http_method=http_method, path=path, body=str_body)
    return str_body.encode('utf-8'), salt, timestamp, signature

def create_headers(http_method, url,  body=None):
    body, salt, timestamp, signature = pre_call(http_method=http_method, path=url, body=body)
    return body, current_sig_headers(salt, timestamp, signature)

def make_request(method,path,body=""):
    body, headers = create_headers(method, base_url + path, body)

    if method.upper() == 'GET':
        response = requests.get(base_url + path,headers=headers)
        print("Everything is fine till here")
    elif method.upper() == 'PUT':
        response = requests.put(base_url + path, data=body, headers=headers)
    elif method.upper() == 'DELETE':
        response = requests.delete(base_url + path, data=body, headers=headers)
    else:
        response = requests.post(base_url + path, data=body, headers=headers)

    #Un comment this in production time.
    # if response.status_code != 200:
    #     raise TypeError(response, method,base_url + path)
    return json.loads(response.content)


@login_required(login_url='Login')
def PaymentDirection(request,price):
    wallet_body = {
        "amount": price,
        "currency": "USD",
        "country":"US",
        "complete_payment_url":"store:Sucess",
        #Change this github link at the time of production. to the website link
        #Rapyd do not allow urls of local host. Thats why we kept github here
        "complete_checkout_url":"https://www.github.com/anirudh3167",
        "error_payment_url":"store:Failed"
    }
    response = make_request(method='post',path='/v1/checkout',body=wallet_body)
    #print(response)
    hosted_url = response['data']['redirect_url']
    #print("REDIRECT_URL:",hosted_url)

    #temporarily being used here. i.e. clearing cart after payment
    user = request.user
    CartItems.objects.filter(owner=user).delete()

    return redirect(hosted_url)

def PaymentSucess(request):
    user = request.user
    CartItems.objects.filter(owner=user).delete()
    return render(request,'pay_sucess.html')

def PaymentFailed(request):
    return render(request,"pay_fail.html")