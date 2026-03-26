from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from .middlewares import auth, loggedin_auth
from .forms import SellerSignupForm, SellerLoginForm


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
