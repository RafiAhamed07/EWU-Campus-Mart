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
            'offer_price',
            'is_available',
            'notes',
            'product_desription',
            'color_variant',
            'size_variant'
        ]
        

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep current image on edit if seller does not upload a new one.
        if self.instance and self.instance.pk:
            self.fields['category_image'].required = False

    class Meta:
        model = Category
        fields = ['category_name', 'category_image']