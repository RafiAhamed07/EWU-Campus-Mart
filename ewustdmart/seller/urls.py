from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_home, name='seller-home'),
    path('dashboard/', views.seller_dashboard, name='seller-dashboard'),
    path('login/', views.seller_login, name='seller-login'),
    path('signup/', views.seller_signup, name='seller-signup'),
    path('logout/', views.seller_logout, name='seller-logout'),
]


