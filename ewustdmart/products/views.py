# Create your views here.
from django.shortcuts import render, redirect
from .forms import ProductForm

def add_product(request):
    if not request.user.is_seller:
        return redirect('seller-login')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # 🔥 important
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller-dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})