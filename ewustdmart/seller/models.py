from django.db import models
from django.utils import timezone
from buyer.models import CustomUser
from base.models import BaseModel


class SellerBanner(BaseModel):
	seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="banner_requests")
	banner_image = models.ImageField(upload_to="banners/")
	banner_text = models.CharField(max_length=140, blank=True)
	is_approved = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.seller.username} banner"