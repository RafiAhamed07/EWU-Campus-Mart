from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from .middlewares import auth, loggedin_auth
from .forms import SellerSignupForm, SellerLoginForm
from products.models import Product, Category, ProductImage
from django.shortcuts import get_object_or_404
from orders.models import OrderItem

# Create your views here.
def seller_home(request):
    return render(request, "seller_home.html")


@auth
def seller_dashboard(request):
    return render(request, "seller_dashboard.html")


@loggedin_auth
def seller_login(request):
    if request.method == "POST":
        form = SellerLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_seller:
                login(request, user)
                return redirect("seller-dashboard")
    else:
        initial_data = {
            "username": "",
            "password": "",
        }
        form = SellerLoginForm(initial=initial_data)
    return render(request, "seller_login.html", {"form": form})


@loggedin_auth
def seller_signup(request):
    if request.method == "POST":
        form = SellerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = True
            user.shop_name = form.cleaned_data["shop_name"]
            user = form.save()
            login(request, user)
            return redirect("seller-dashboard")
    else:
        initial_data = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "std_id": "",
            "shop_name": "",
            "password1": "",
            "password2": "",
        }
        form = SellerSignupForm(initial=initial_data)
    return render(request, "seller_signup.html", {"form": form})


def seller_logout(request):
    logout(request)
    return redirect("seller-home")


@auth
def seller_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, "seller_products.html", {"products": products})


@auth
def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category_id = request.POST.get("category")

        category = Category.objects.get(uid=category_id)

        # ✅ Create product
        product = Product.objects.create(
            seller=request.user,
            product_name=name,
            price=price,
            product_desription=description,
            category=category
        )

        # 🔥 HANDLE MULTIPLE IMAGES
        images = request.FILES.getlist('images')

        for img in images:
            ProductImage.objects.create(
                product=product,
                image=img
            )

        return redirect("seller-products")

    return render(request, "add_product.html", {"categories": categories})

# ✅ Delete product
@auth
def delete_product(request, uid):
    product = get_object_or_404(Product, uid=uid, seller=request.user)
    product.delete()
    return redirect("seller-products")


@auth
def seller_orders(request):
    orders = OrderItem.objects.filter(product__seller=request.user).order_by('-created_at')
    
    return render(request, "seller_orders.html", {"orders": orders})



def update_order_item_status(request, uid, status):
    item = get_object_or_404(OrderItem, uid=uid, product__seller=request.user)

    if status in ['accepted', 'rejected', 'shipped', 'delivered']:
        item.status = status
        item.save()

        # 🔥 CALL HERE
        item.order.update_status()

    return redirect('seller-orders')



