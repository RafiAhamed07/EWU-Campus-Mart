# admin.py
from django.contrib import admin
from .models import CustomUser, SellerRequest

admin.site.register(CustomUser)
admin.site.register(SellerRequest)
