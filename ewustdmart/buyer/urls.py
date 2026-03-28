from django.urls import path
from . import views

urlpatterns = [
    path("", views.buyer_home, name="buyer-home"),
    path("dashboard/", views.buyer_dashboard, name="buyer-dashboard"),
    path("login/", views.buyer_login, name="buyer-login"),
    path("signup/", views.buyer_signup, name="buyer-signup"),
    path("logout/", views.buyer_logout, name="buyer-logout"),
    path('product/<slug:slug>/', views.product_detail, name='product-detail'),
]
