# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser_buyer

# class CustomUserInline(admin.StackedInline):
#     model = CustomUser_buyer
#     can_delete = False
#     verbose_name_plural = 'Profile'

# class CustomUserAdmin(UserAdmin):
#     inlines = (CustomUserInline,)
#     list_display = UserAdmin.list_display + ('get_std_id',)

#     def get_std_id(self, obj):
#         return obj.customuser_buyer.std_id
#     get_std_id.short_description = 'Student ID'

admin.site.register(CustomUser_buyer)