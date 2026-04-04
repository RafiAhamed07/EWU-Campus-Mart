from django.db import models
from base.models import BaseModel
from buyer.models import CustomUser
from products.models import Product


class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    total_price = models.IntegerField()

    STATUS_CHOICES = (
        ('pending', 'Pending'),        # order placed
        ('accepted', 'Accepted'),      # seller accepted
        ('rejected', 'Rejected'),      # seller rejected
        ('shipped', 'Shipped'),        # seller shipped
        ('delivered', 'Delivered'),    # delivered
        ('cancelled', 'Cancelled'),    # buyer cancelled
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    address = models.TextField()
    phone = models.CharField(max_length=15)

    # 🔥 NEW FIELDS
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, default='SSLCommerz')

    def __str__(self):
        return f"{self.uid} - {self.status}"
    def update_status(self):
        items = self.order_items.all()

        if all(item.status == 'delivered' for item in items):
            self.status = 'paid'

        elif any(item.status == 'rejected' for item in items):
            self.status = 'failed'

        elif all(item.status in ['accepted', 'shipped', 'delivered'] for item in items):
            self.status = 'paid'

        else:
            self.status = 'pending'

        self.save()
    
    
    
    
    
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_option = models.ForeignKey(
        'products.ProductOption',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )

    quantity = models.IntegerField()
    price = models.IntegerField()  # price at purchase time

    # 🔥 NEW: seller-specific status
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def get_total_price(self):
        return self.price * self.quantity
    

    def __str__(self):
        return f"{self.product.product_name} ({self.status})"