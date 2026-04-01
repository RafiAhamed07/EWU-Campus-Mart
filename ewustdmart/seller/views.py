from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from .middlewares import auth, loggedin_auth
from .forms import SellerSignupForm, SellerLoginForm
from products.models import Product, Category, ProductImage
from django.shortcuts import get_object_or_404
from orders.models import OrderItem

from products.models import Category
from products.forms import CategoryForm
from .middlewares import auth
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order

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

        category_id = request.POST.get("category")
        product.category = Category.objects.get(uid=category_id)

        product.save()

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
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('seller-categories')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})


@auth
def seller_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


@auth
def edit_category(request, uid):
    category = get_object_or_404(Category, uid=uid)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('seller-categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'add_category.html', {'form': form})

@auth
def delete_category(request, uid):
    category = get_object_or_404(Category, uid=uid)
    category.delete()
    return redirect('seller-categories')

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

