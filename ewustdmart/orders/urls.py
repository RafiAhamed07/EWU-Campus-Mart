from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order-success"),
    path("my-orders/", views.my_orders, name="my-orders"),
    path("order/<uuid:uid>/", views.order_detail, name="order-detail"),
    path("cancel/<uuid:uid>/", views.cancel_order, name="cancel-order"),
    path("pay/", views.initiate_payment, name="initiate-payment"),
    
    path("callback/success/", views.payment_success, name="payment-success"),
    path("callback/fail/", views.payment_fail, name="payment-fail"),
    path("callback/cancel/", views.payment_cancel, name="payment-cancel"),
]
