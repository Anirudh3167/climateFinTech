from rest_framework.response import Response
from rest_framework.decorators import api_view
from Backend.models import CartItems
from .serializers import CartSerializer

#for communicating with other APIs
from pprint import pprint
import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests

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

@api_view(['GET','POST','PUT','DELETE'])
def RapydTesting(request,country,currency):
    # Rapyd_url = base_url
    # response = requests.get(Rapyd_url)

    #path here will get auto added to the base_url path in make_requests section.
    #For getting the payment methods available
    response = make_request(method='get',
                        path=f'/v1/payment_methods/countries/{country}?currency={currency}')
    #pprint(response)
    return Response(response)

@api_view(['GET','POST','PUT','DELETE'])
def RapydPaymentFields(request,method_name):
    #For getting the required fields for payment method.
    #For IT ->Italy use payment_method_type as 'it_visa_card'
    payment_method_type = method_name
    response = make_request(method='get',
                        path=f'/v1/payment_methods/required_fields/{payment_method_type}')
    return Response(response)


@api_view(['GET','POST','PUT','DELETE'])
def CreateCustomer(request):

    #For sg_credit_cup_card
    body = {
        "name": "John Doe",
        "payment_method": {
            "type": "sg_credit_cup_card",
            "fields": {
                "number": "4111111111111111",
                "expiration_month": "10",
                "expiration_year": "23",
                "cvv": "123",
                "name": "John Doe"
            },
            "complete_payment_url": "https://complete.rapyd.net/",
            "error_payment_url": "https://error.rapyd.net/"
        }
    }

    #for e-wallet
    body1 = {
    "business_vat_id": "123456789",
    "email": "johndoe@rapyd.net",
    "ewallet": "ewallet_ebfe4c4f4d36b076a21369fb0d055f3e",
    "invoice_prefix": "JD-",
    "metadata": {
    	"merchant_defined": True
    },
    "name": "John Doe",
    "phone_number": "+14155559993"
}
    response = make_request(method='post',path=f'/v1/customers',body=body)
    return Response(response)

@api_view(['GET','POST','PUT','DELETE'])
def CreatePayments(request):
    #cash payment
    # body ={
    #     'amount':'230',
    #     'currency':'USD',
    #     'payment_method': {
    #         "type":"us_duanereade_cash"
    #     }
    # }
    body={
        "amount": 100,
        "currency": "USD",
        "description": "Payment method token",
        "customer": "cus_e9fe450a046b6e7f2b54aa12abdc13d1",
        #"payment_method": {"type":"card"},
        # "ewallets": [{
        #         "ewallet": "ewallet_1290eef66d0b84ece177a3f5bd8fb0c8",
        #         "percentage": 100
        #     }
        # ],
        "metadata": {
            "merchant_defined": True
        }
    }

    #card payments
    payment_body = {
        'amount': 30,
        'currency': 'INR',
        'payment_method': {
            'type': 'in_visa_credit_card',
            'fields': {
                'name':'annonymous',
                'number': '4111111111111111',
                'expiration_month': '10',
                'expiration_year': '23',
                'cvv': '123'
            }
        },
        'error_payment_url': 'https://rapyd.net',
        'capture': True
    }

    #wallet payments
    wallet_body = {
        "amount": 19.99,
        "currency": "SGD",
        "payment_method": {
            "type": "sg_grabpay_ewallet",
            "fields": {}
        },
        "complete_payment_url":"http://www.rapyd.net/complete",
        "error_payment_url":"http://www.rapyd.net/error"
    }
    response = make_request(method='post',path='/v1/payments',body=wallet_body)

    return Response(response)

@api_view(['GET','POST'])
def WalletTransfer(request):
    body = {
    "source_ewallet": "ewallet_5bd04f949e3a8ae23bcfe679b4a2b8b3",
    "amount": 15,
    "currency": "USD",
    "destination_ewallet": "ewallet_e9e973e1c8b9cd030ce573157702ff78",
    "metadata":
        {
            "merchant_defined": True
        }
    }
    response = make_request(method='post',path=f'/v1/payments',body=body)
    return Response(response)


#####################################################
# WALLET
#####################################################
@api_view(['GET','POST','PUT','DELETE'])
def WalletStatus(request,status):
    #status can either be enable or disable.
    wallet_id = 'ewallet_5bd04f949e3a8ae23bcfe679b4a2b8b3'
    body = {'ewallet': wallet_id}
    disable_results = make_request(method='put', path=f'/v1/user/{status}', body=body)

    return Response(disable_results)

@api_view(['GET','POST'])
def AddFunds(request,amt):
    wallet = 'ewallet_5bd04f949e3a8ae23bcfe679b4a2b8b3'
    body = {
        "ewallet": wallet,
        "amount": amt,
        "currency": "INR",
        "metadata": {
            "merchant_defined": True
        }
    }
    results = make_request(method='post', path='/v1/account/deposit', body=body)
    return Response(results)

@api_view(['GET','POST'])
def withdrawFunds(request,amt):
    wallet = 'ewallet_5bd04f949e3a8ae23bcfe679b4a2b8b3'
    body = {
        "ewallet": wallet,
        "amount": amt,
        "currency": "INR",
        "metadata": {
            "merchant_defined": True
        }
    }
    results = make_request(method='post', path='/v1/account/withdraw', body=body)
    return Response(results)

@api_view(['GET','POST'])
def AddFundsDetails(request,id):
    results= make_request(method='get',path=f'/v1/account/deposit/{id}')
    return Response(results)

@api_view(['GET','POST'])
def RemoveFundsDetails(request,id):
    results= make_request(method='get',path=f'/v1/account/withdraw/{id}')
    return Response(results)

@api_view(['GET','POST'])
def TransferFunds(request,amt):
    body = {
        "amount":amt,
        "currency":"EUR",
        "source_ewallet": 'ewallet_d53a11ea77aec2322e1851175cd8c947',
        "destination_ewallet":'ewallet_8eb22d9d7d63f6f61893e2b9d164b7cf'
    }
    results= make_request(method='get',path=f'/v1/account/transfer',body=body)
    return Response(results)

@api_view(['GET','POST'])
def CreateWallet(request,type):
    if type=="personal":
        # Creating personal wallet
        personal_wallet = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "ewallet_reference_id": "John-Doe-02152020",
            "metadata": {
                "merchant_defined": True
            },
            "phone_number": "",
            "type": "person",
            "contact": {
                "phone_number": "+14155551234",
                "email": "johndoe1@rapyd.net",
                "first_name": "John",
                "last_name": "Doe",
                "mothers_name": "Jane Smith",
                "contact_type": "personal",
                "address": {
                    "name": "John Doe",
                    "line_1": "123 Main Street",
                    "line_2": "",
                    "line_3": "",
                    "city": "Anytown",
                    "state": "NY",
                    "country": "US",
                    "zip": "12345",
                    "phone_number": "+14155551234",
                    "metadata": {},
                    "canton": "",
                    "district": ""
                },
                "identification_type": "PA",
                "identification_number": "1234567890",
                "date_of_birth": "11/22/2000",
                "country": "US",
                "metadata": {
                    "merchant_defined": True
                }
            }
        }

        personal_wallet_results = make_request(method='post', path='/v1/user', body=personal_wallet)
        return Response(personal_wallet_results)
    else:
        # Creating company ewallet
        company_wallet = {
            "first_name": "Four Star Professional Services",
            "last_name": "",
            "ewallet_reference_id": "e-77641",
            "metadata": {
                "merchant_defined": True
            },
            "type": "company",
            "contact": {
                "phone_number": "+14155551234",
                "email": "johndoe1@rapyd.net",
                "first_name": "John",
                "last_name": "Doe",
                "contact_type": "business",
                "address": {
                    "name": "John Doe",
                    "line_1": "123 Main Street",
                    "line_2": "",
                    "line_3": "",
                    "city": "Anytown",
                    "state": "NY",
                    "country": "US",
                    "zip": "12345",
                    "phone_number": "+14155551234",
                    "metadata": {},
                    "canton": "",
                    "district": ""
                },
                "identification_type": "PA",
                "identification_number": "1234567890",
                "date_of_birth": "11/22/2000",
                "country": "US",
                "metadata": {
                    "merchant_defined": True
                },
                "business_details": {
                    "entity_type": "association",
                    "name": "Four Star Professional Services",
                    "registration_number": "4234567779",
                    "industry_category": "company",
                    "industry_sub_category": "home services",
                    "address": {
                        "name": "John Doe",
                        "line_1": "1234 Main Street",
                        "line_2": "Suite 1200",
                        "line_3": "",
                        "city": "Anytown",
                        "state": "NY",
                        "country": "US",
                        "zip": "10101",
                        "phone_number": "14155557779",
                        "metadata": {
                            "merchant_defined": True
                        }
                    }
                }
            }
        }

        company_wallet_results = make_request(method='post', path='/v1/user', body=company_wallet)
        return Response(company_wallet_results)

@api_view(['GET','POST'])
def RetriveWallet(request,wallet):
    results = make_request(method='get', path=f'/v1/user/{wallet}')
    return Response(results)

@api_view(['GET','POST'])
def ListWallets(request):
    results = make_request(method='get', path='/v1/user/wallets')
    return Response(results)

@api_view(['GET','POST'])
def DeleteWallet(request,wallet):
    results = make_request(method='post', path=f'/v1/user/{wallet}')
    return Response(results)
#####################################################
# CART RELATED REQUESTS
#####################################################
@api_view(['GET'])
def getData(request):
    items = CartItems.objects.all()
    serializer = CartSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def PostData(request):
    serializer = CartSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


