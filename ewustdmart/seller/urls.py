from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_home, name='seller-home'),
    path('dashboard/', views.seller_dashboard, name='seller-dashboard'),

    path('products/', views.seller_products, name='seller-products'),
    path('add-product/', views.add_product, name='add-product'),
    path('delete-product/<uuid:uid>/', views.delete_product, name='delete-product'),

    path('login/', views.seller_login, name='seller-login'),
    path('signup/', views.seller_signup, name='seller-signup'),
    path('logout/', views.seller_logout, name='seller-logout'),
    
    path('orders/', views.seller_orders, name='seller-orders'),
]


