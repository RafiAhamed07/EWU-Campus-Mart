from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .middlewares import auth, loggedin_auth
from .forms import SellerSignupForm, SellerLoginForm
from products.models import Product, Category, ProductImage, ProductOption
from django.shortcuts import get_object_or_404
from orders.models import OrderItem
from orders.models import Order
from .models import SellerBanner

# Create your views here.
def seller_home(request):
    return render(request, "seller_home.html")


@auth
@auth
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)

    order_items = OrderItem.objects.filter(product__seller=request.user)

    total_products = products.count()
    total_orders = order_items.count()

    total_revenue = sum(
        item.get_total_price() for item in order_items if item.status != 'cancelled'
    )

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'banner_requests': SellerBanner.objects.filter(seller=request.user),
    }

    return render(request, "seller_dashboard.html", context)


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


def _parse_variant_rows(raw_text):
    variants = []
    if not raw_text:
        return variants

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            parts = [part.strip() for part in line.split("|")]
        elif ":" in line:
            parts = [part.strip() for part in line.split(":")]
        else:
            continue
        if len(parts) < 2:
            continue
        name = parts[0]
        price = parts[1]
        offer_price = parts[2] if len(parts) > 2 else ""
        if not name or not price:
            continue

        try:
            parsed_price = int(price)
        except ValueError:
            continue

        parsed_offer = None
        if offer_price:
            try:
                offer_value = int(offer_price)
                if 0 < offer_value < parsed_price:
                    parsed_offer = offer_value
            except ValueError:
                parsed_offer = None

        variants.append((name, parsed_price, parsed_offer))
    return variants


@auth
def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        notes = request.POST.get("notes")
        variant_rows = request.POST.get("variant_rows", "")

        uploaded_images = [
            request.FILES.get("image_1"),
            request.FILES.get("image_2"),
            request.FILES.get("image_3"),
            request.FILES.get("image_4"),
        ]
        uploaded_images = [img for img in uploaded_images if img]

        if len(uploaded_images) > 4:
            messages.error(request, "You can upload up to 4 images only.")
            return render(request, "add_product.html", {"categories": categories})

        category = Category.objects.get(uid=category_id)

        # ✅ Create product
        product = Product.objects.create(
            seller=request.user,
            product_name=name,
            price=price,
            product_desription=description,
            category=category,
            offer_price=None,
            is_available=True,
            notes=notes,
        )

        for variant_name, variant_price, variant_offer_price in _parse_variant_rows(variant_rows):
            ProductOption.objects.create(
                product=product,
                option_name=variant_name,
                price=variant_price,
                offer_price=variant_offer_price,
            )

        # Save up to 4 uploaded images for this product.
        for img in uploaded_images:
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
def update_product_offer(request, uid):
    product = get_object_or_404(Product, uid=uid, seller=request.user)
    if request.method == "POST":
        if product.options.exists():
            messages.info(request, "This product has quantity options. Set offer per quantity in Edit Product (Option|BasePrice|OfferPrice).")
            return redirect("seller-products")

        offer_raw = (request.POST.get("offer_price") or "").strip()
        if not offer_raw:
            product.offer_price = None
        else:
            try:
                offer_value = int(offer_raw)
            except ValueError:
                offer_value = None

            if offer_value and 0 < offer_value < product.price:
                product.offer_price = offer_value
            else:
                product.offer_price = None

        product.save(update_fields=["offer_price", "updated_at"])
    return redirect("seller-products")


@auth
def update_product_availability(request, uid):
    product = get_object_or_404(Product, uid=uid, seller=request.user)
    if request.method == "POST":
        product.is_available = request.POST.get("is_available") == "on"
        product.save(update_fields=["is_available", "updated_at"])
    return redirect("seller-products")


from orders.models import OrderItem

@auth
def seller_orders(request):
    orders = OrderItem.objects.filter(product__seller=request.user)\
            .select_related('product', 'order')\
            .order_by('-created_at')

    return render(request, 'seller_orders.html', {'orders': orders})



def update_order_item_status(request, uid, status):
    item = get_object_or_404(OrderItem, uid=uid, product__seller=request.user)

    if status in ['accepted', 'rejected', 'shipped', 'delivered']:
        item.status = status
        item.save()

        # 🔥 CALL HERE
        item.order.update_status()

    return redirect('seller-orders')



@auth
def edit_product(request, uid):
    product = get_object_or_404(Product, uid=uid, seller=request.user)
    categories = Category.objects.all()

    if request.method == "POST":
        product.product_name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.product_desription = request.POST.get("description")
        product.notes = request.POST.get("notes")
        product.offer_price = request.POST.get("offer_price") or None
        product.is_available = request.POST.get("is_available") == "on"

        category_id = request.POST.get("category")
        product.category = Category.objects.get(uid=category_id)

        product.save()

        product.options.all().delete()
        for variant_name, variant_price, variant_offer_price in _parse_variant_rows(request.POST.get("variant_rows", "")):
            ProductOption.objects.create(
                product=product,
                option_name=variant_name,
                price=variant_price,
                offer_price=variant_offer_price,
            )

        # 🔥 ADD NEW IMAGES (optional)
        images = request.FILES.getlist("images")
        for img in images:
            ProductImage.objects.create(product=product, image=img)

        return redirect("seller-products")

    return render(request, "edit_product.html", {
        "product": product,
        "categories": categories
    })


@auth
def delete_product_image(request, uid):
    image = get_object_or_404(ProductImage, uid=uid, product__seller=request.user)
    product_uid = image.product.uid
    image.delete()

    return redirect("edit-product", uid=product_uid)

@auth
def accept_order(request, uid):
    item = get_object_or_404(OrderItem, uid=uid, product__seller=request.user)
    item.status = 'accepted'
    item.save()
    return redirect('seller-orders')

@auth
def ship_order(request, uid):
    item = get_object_or_404(OrderItem, uid=uid, product__seller=request.user)
    item.status = 'shipped'
    item.save()
    return redirect('seller-orders')


@auth
def ship_order(request, uid):
    item = get_object_or_404(OrderItem, uid=uid, product__seller=request.user)
    item.status = 'shipped'
    item.save()
    return redirect('seller-orders')

@auth
def cancel_order_item(request, uid):
    item = get_object_or_404(OrderItem, uid=uid, product__seller=request.user)
    item.status = 'cancelled'
    item.save()
    return redirect('seller-orders')


@auth
def update_order_status(request, uid, status):
    order = get_object_or_404(Order, uid=uid)
    
    allowed_status = ['accepted', 'rejected', 'shipped', 'delivered']
    if status in allowed_status:
        order.status = status
        order.save()
    
    return redirect('seller-orders')


@auth
def request_banner(request):
    if request.method == "POST":
        banner = SellerBanner.objects.create(
            seller=request.user,
            banner_image=request.FILES.get("banner_image"),
            banner_text=request.POST.get("banner_text", ""),
            is_approved=True,
        )
        return redirect("seller-dashboard")

    return render(request, "banner_request.html")


@auth
def delete_banner(request, uid):
    banner = get_object_or_404(SellerBanner, uid=uid, seller=request.user)

    if request.method == "POST":
        banner.delete()
        messages.success(request, "Banner deleted successfully.")

    return redirect("seller-dashboard")

