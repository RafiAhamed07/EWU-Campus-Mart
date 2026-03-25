# from django.db import models
# from django.utils import timezone
# from django.core.exceptions import ValidationError

# def validate_specific_domain(value):
#     # Change '@example.com' to your required domain
#     if not value.endswith('@std.ewubd.edu') and not value.endswith('@ewubd.edu'):
#         raise ValidationError(
#             'Only institutional email addresses are allowed.'
#         )

# # Create your models here.
# class Buyer_user(models.Model):
#     username = models.CharField(max_length=100)
#     std_id = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(validators=[validate_specific_domain])
#     password = models.CharField(max_length=128)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.name