from django.urls import path
from . import views

urlpatterns = [
    #Rapyd_URLS
    path('country-<str:country>-<str:currency>',views.RapydTesting),
    path('payment-fields/<str:method_name>',views.RapydPaymentFields),
    path('wallet-<str:status>',views.WalletStatus),
    path('create-payment/',views.CreatePayments),
    path('walletpayment',views.WalletTransfer),

    #wallet
    path('add-funds-<str:amt>',views.AddFunds),
    path('withdraw-funds-<str:amt>',views.withdrawFunds),
    path('add_funds-details-<str:id>',views.AddFundsDetails),
    path('remove_funds-details-<str:id>',views.RemoveFundsDetails),
    path('transfer-funds-<str:amt>',views.TransferFunds),
    path('create-wallet-<str:type>',views.CreateWallet),
    path('retrive-wallet-<str:wallet>',views.RetriveWallet),
    path('list-wallets',views.ListWallets),
    path('delete-wallet=<str:wallet>',views.DeleteWallet),
    #For creating customer
    path('create-customer',views.CreateCustomer),

    #cart_URLS
    path('get/',views.getData),
    path('add/',views.PostData),
]