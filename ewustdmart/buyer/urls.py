from django.urls import path
from . import views

urlpatterns = [
    path("", views.buyer_home, name="buyer-home"),
    path("dashboard/", views.buyer_dashboard, name="buyer-dashboard"),
    path("profile/", views.buyer_profile, name="buyer-profile"),
    path("profile/update/", views.buyer_profile_update, name="buyer-profile-update"),
    path("seller/<uuid:uid>/", views.seller_profile, name="seller-profile"),
    path("login/", views.buyer_login, name="buyer-login"),
    path("signup/", views.buyer_signup, name="buyer-signup"),
    path("logout/", views.buyer_logout, name="buyer-logout"),
    path('product/<slug:slug>/', views.product_detail, name='product-detail'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.view_cart, name='view-cart'),
    path('cart/update/<uuid:uid>/<str:action>/', views.update_cart_item, name='update-cart'),
    path('cart/remove/<uuid:uid>/', views.remove_cart_item, name='remove-cart'),
]
