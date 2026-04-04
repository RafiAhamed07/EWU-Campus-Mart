from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .middlewares import auth, loggedin_auth
from .forms import BuyerSignupForm, BuyerLoginForm, BuyerProfileForm, SellerRequestForm
from .models import SellerRequest, CustomUser
from products.models import Product, Cart, CartItem, Category, ProductOption
from seller.models import SellerBanner

# Create your views here.
def buyer_home(request):
    return render(request, "buyer_home.html")


@auth
def buyer_dashboard(request):
    selected_category = request.GET.get("category", "all")
    categories = Category.objects.all().order_by("category_name")

    products = Product.objects.select_related("category", "seller").prefetch_related("product_images")
    if selected_category != "all":
        products = products.filter(category__slug=selected_category)

    approved_banners = SellerBanner.objects.filter(is_approved=True).select_related("seller")

    return render(request, 'buyer_dashboard.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'banners': approved_banners,
    })


@loggedin_auth
def buyer_login(request):
    if request.method == "POST":
        form = BuyerLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_buyer:
                login(request, user)
                return redirect("buyer-dashboard")
    else:
        initial_data = {
            "username": "",
            "password": "",
        }
        form = BuyerLoginForm(initial=initial_data)
    return render(request, "buyer_login.html", {"form": form})


@loggedin_auth
def buyer_signup(request):
    if request.method == "POST":
        form = BuyerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_buyer = True
            user.std_id = form.cleaned_data["std_id"]
            user = form.save()
            login(request, user)
            return redirect("buyer-dashboard")
    else:
        initial_data = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "std_id": "",
            "password1": "",
            "password2": "",
        }
        form = BuyerSignupForm(initial=initial_data)
    return render(request, "buyer_signup.html", {"form": form})


def buyer_logout(request):
    logout(request)
    return redirect("buyer-home")


@auth
def buyer_profile(request):
    latest_request = SellerRequest.objects.filter(user=request.user).first()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "request_seller":
            request_form = SellerRequestForm(request.POST)

            if request.user.is_seller:
                messages.info(request, "You are already a seller.")
                return redirect("buyer-profile")

            has_pending = SellerRequest.objects.filter(
                user=request.user,
                status=SellerRequest.STATUS_PENDING,
            ).exists()
            if has_pending:
                messages.info(request, "You already have a pending seller request.")
                return redirect("buyer-profile")

            if request_form.is_valid():
                seller_request = request_form.save(commit=False)
                seller_request.user = request.user
                seller_request.status = SellerRequest.STATUS_APPROVED
                seller_request.save()

                request.user.is_buyer = True
                request.user.is_seller = True
                request.user.shop_name = seller_request.shop_name
                request.user.save(update_fields=["is_buyer", "is_seller", "shop_name"])

                messages.success(request, "You are now a seller.")
                return redirect("buyer-profile")
        else:
            request_form = SellerRequestForm()
    else:
        request_form = SellerRequestForm()

    context = {
        "request_form": request_form,
        "latest_request": latest_request,
    }
    return render(request, "buyer_profile.html", context)


@auth
def buyer_profile_update(request):
    if request.method == "POST":
        profile_form = BuyerProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("buyer-profile")
    else:
        profile_form = BuyerProfileForm(instance=request.user)

    return render(request, "buyer_profile_update.html", {"profile_form": profile_form})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    seller_products = Product.objects.filter(seller=product.seller, category=product.category).exclude(uid=product.uid)
    seller_categories = Product.objects.filter(seller=product.seller).values_list("category__category_name", flat=True).distinct()
    return render(request, 'product_detail.html', {
        'product': product,
        'seller_products': seller_products,
        'seller_categories': seller_categories,
        'seller': product.seller,
    })


@auth
def seller_profile(request, uid):
    seller = get_object_or_404(
        CustomUser,
        uid=uid,
        is_seller=True,
    )
    selected_category = request.GET.get("category", "all")
    products = Product.objects.filter(seller=seller).select_related("category")
    categories = Category.objects.filter(products__seller=seller).distinct().order_by("category_name")

    if selected_category != "all":
        products = products.filter(category__slug=selected_category)

    return render(request, "seller_profile.html", {
        "seller": seller,
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
    })

def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user
    selected_option = None
    quantity = 1

    if request.method == "POST":
        option_id = request.POST.get("option")
        if option_id:
            selected_option = get_object_or_404(ProductOption, uid=option_id, product=product)
        try:
            quantity = max(1, int(request.POST.get("quantity", 1)))
        except (TypeError, ValueError):
            quantity = 1

    unit_price = selected_option.display_price if selected_option else product.display_price

    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        product_option=selected_option,
    )

    cart_item.unit_price = unit_price

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('view-cart')

def update_cart_item(request, uid, action):
    cart_item = get_object_or_404(CartItem, uid=uid)

    if action == 'increase':
        cart_item.quantity += 1

    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('view-cart')

    cart_item.save()
    return redirect('view-cart')


def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    total = 0
    if cart:
        for item in cart.cart_items.all():
            total += item.get_total_price()

    return render(request, 'cart.html', {
        'cart': cart,
        'total': total
    })
    
def remove_cart_item(request, uid):
    cart_item = get_object_or_404(CartItem, uid=uid)
    cart_item.delete()
    return redirect('view-cart')