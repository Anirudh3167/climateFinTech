from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests

# Create your views here.

def Home(request):
    return render(request,'storeHome.html')

def About(request):
    return render(request,'about_climate.html')

def ProductDetails(request):
    context = {"acd":"acd"}
    return render(request,'storePrductDetails.html',context)

@login_required(login_url='Login')
def Cart(request):
    return render(request,'storeCart.html')

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
def PaymentDirection(request):
    wallet_body = {
        "amount": 50,
        "currency": "INR",
        "country":"IN",
        "complete_payment_url":"store:Sucess",
        #Change this github link at the time of production. to the website link
        #Rapyd do not allow urls of local host. Thats why we kept github here
        "complete_checkout_url":"https://www.github.com/anirudh3167",
        "error_payment_url":"store:Failed"
    }
    response = make_request(method='post',path='/v1/checkout',body=wallet_body)
    print(response)
    hosted_url = response['data']['redirect_url']
    print("REDIRECT_URL:",hosted_url)
    return redirect(hosted_url)

def PaymentSucess(request):
    return render(request,'pay_sucess.html')

def PaymentFailed(request):
    return render(request,"pay_fail.html")