from django.db import models
from base.models import BaseModel
from buyer.models import CustomUser
from products.models import Product


class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    total_price = models.IntegerField()

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    address = models.TextField()
    phone = models.CharField(max_length=15)

    # 🔥 NEW FIELDS
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, default='SSLCommerz')

    def __str__(self):
        return f"{self.uid} - {self.status}"
    
    
    
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.IntegerField()  # price at purchase time

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product.product_name