from django import forms
from .models import Product
from .models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'category',
            'price',
            'product_desription',
            'color_variant',
            'size_variant'
        ]
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_image']