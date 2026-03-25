from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .middlewares import auth, loggedin_auth

# Create your views here.
def buyer_home(request):
    return render(request, 'buyer_home.html')

@auth
def buyer_dashboard(request):
    return render(request, 'buyer_dashboard.html')

@loggedin_auth
def buyer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('buyer-dashboard')
    else:
        initial_data = {
            'username': '',
            'password': '',
        }
        form = AuthenticationForm(initial = initial_data)
    return render(request, 'buyer_login.html', {'form': form})

@loggedin_auth
def buyer_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('buyer-dashboard')
    else:
        initial_data = {
            'username': '',
            'password1': '',
            'password2': '',
        }
        form = UserCreationForm(initial = initial_data)
    return render(request, 'buyer_signup.html', {'form': form})

def buyer_logout(request):
    logout(request)
    return redirect('buyer-home')


