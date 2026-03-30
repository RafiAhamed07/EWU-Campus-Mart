from django.shortcuts import render, redirect, get_object_or_404
from products.models import Cart
from .models import Order, OrderItem

import uuid
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.cart_items.all():
        return redirect("view-cart")

    total = sum(item.get_total_price() for item in cart.cart_items.all())

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        # Create Order
        order = Order.objects.create(
            user=request.user, total_price=total, address=address, phone=phone
        )

        # Create Order Items
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Clear cart
        cart.cart_items.all().delete()

        return redirect("order-success")

    return render(request, "checkout.html", {"cart": cart, "total": total})


def order_success(request):
    return render(request, "order_success.html")


def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})


def order_detail(request, uid):
    order = get_object_or_404(Order, uid=uid, user=request.user)
    return render(request, "order_detail.html", {"order": order})


def cancel_order(request, uid):
    order = get_object_or_404(Order, uid=uid, user=request.user)

    # Only allow cancel if not completed
    if order.status in ["pending", "processing"]:
        order.status = "cancelled"
        order.save()

    return redirect("my-orders")


def initiate_payment(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect("view-cart")

    total = sum(item.get_total_price() for item in cart.cart_items.all())

    tran_id = str(uuid.uuid4())

    order = Order.objects.create(
        user=request.user, total_price=total, transaction_id=tran_id, status="pending"
    )

    for item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    sslcz = SSLCOMMERZ(
        {
            "store_id": settings.SSL_STORE_ID,
            "store_pass": settings.SSL_STORE_PASSWORD,
            "issandbox": True,
        }
    )

    post_body = {
        "total_amount": total,
        "currency": "BDT",
        "tran_id": tran_id,
        "success_url": request.build_absolute_uri("/orders/callback/success/"),
        "fail_url": request.build_absolute_uri("/orders/callback/fail/"),
        "cancel_url": request.build_absolute_uri("/orders/callback/cancel/"),
        "cus_name": request.user.username,
        "cus_email": request.user.email,
        "cus_phone": (
            request.user.phone if hasattr(request.user, "phone") else "01700000000"
        ),
        "cus_add1": "Dhaka",
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "product_name": "EWU Order",
        "product_category": "General",
        "product_profile": "general",
    }

    response = sslcz.createSession(post_body)

    return redirect(response["GatewayPageURL"])


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_success(request):
    tran_id = request.POST.get("tran_id")
    order = Order.objects.filter(transaction_id=tran_id).first()
    if order:
        order.status = "paid"
        order.save()
        # Clear cart items
        cart = Cart.objects.filter(user=order.user).first()
        if cart:
            cart.cart_items.all().delete()
    return render(request, "success.html")


@csrf_exempt
def payment_fail(request):
    tran_id = request.POST.get("tran_id")
    order = Order.objects.filter(transaction_id=tran_id).first()
    if order:
        order.status = "failed"
        order.save()
    return render(request, "fail.html")


@csrf_exempt
def payment_cancel(request):
    tran_id = request.POST.get("tran_id")
    order = Order.objects.filter(transaction_id=tran_id).first()
    if order:
        order.status = "cancelled"
        order.save()
    return render(request, "cancel.html")
