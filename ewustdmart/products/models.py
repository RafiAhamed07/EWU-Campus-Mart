from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from buyer.models import CustomUser
import uuid

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , null=True , blank=True)
    category_image = models.ImageField(upload_to="categories")


    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category ,self).save(*args , **kwargs)


    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.size_name




class Product(BaseModel):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True  , null=True , blank=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name="products")
    price = models.IntegerField()
    product_desription = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant , blank=True)
    size_variant = models.ManyToManyField(SizeVariant , blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name) + "-" + str(uuid.uuid4())[:6]
        super(Product, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return self.product_name





class ProductImage(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")
    image =  models.ImageField(upload_to="product")
    
    
class Cart(BaseModel):
    user = models.ForeignKey('buyer.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart - {self.user.email}"
    

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = ['cart', 'product']  # 🔥 prevents duplicates

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"