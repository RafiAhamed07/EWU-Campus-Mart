from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['uid', 'user', 'total_price', 'status']
    inlines = [OrderItemInline]


admin.site.register(OrderItem)