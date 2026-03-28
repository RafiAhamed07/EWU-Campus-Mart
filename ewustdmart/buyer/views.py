from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .middlewares import auth, loggedin_auth
from .forms import BuyerSignupForm, BuyerLoginForm
from products.models import Product

# Create your views here.
def buyer_home(request):
    return render(request, "buyer_home.html")


@auth
def buyer_dashboard(request):
    products = Product.objects.all()
    return render(request, 'buyer_dashboard.html', {'products': products})


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

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
  # Debugging line to check if the product is retrieved correctly
    # print(f"Product retrieved: {product.product_name}")
    return render(request, 'product_detail.html', {'product': product})