from django.urls import path
from . import views

urlpatterns = [
    path("", views.seller_home, name="seller-home"),
    path("dashboard/", views.seller_dashboard, name="seller-dashboard"),
    path("products/", views.seller_products, name="seller-products"),
    path("add-product/", views.add_product, name="add-product"),
    path("delete-product/<uuid:uid>/", views.delete_product, name="delete-product"),
    path("login/", views.seller_login, name="seller-login"),
    path("signup/", views.seller_signup, name="seller-signup"),
    path("logout/", views.seller_logout, name="seller-logout"),
    path("edit-product/<uuid:uid>/", views.edit_product, name="edit-product"),
    path(
        "delete-image/<uuid:uid>/",
        views.delete_product_image,
        name="delete-product-image",
    ),
    path("categories/", views.seller_categories, name="seller-categories"),
    path("categories/add/", views.add_category, name="add-category"),
    path("categories/edit/<uuid:uid>/", views.edit_category, name="edit-category"),
    path(
        "categories/delete/<uuid:uid>/", views.delete_category, name="delete-category"
    ),
    path("orders/", views.seller_orders, name="seller-orders"),
    path("orders/accept/<uuid:uid>/", views.accept_order, name="accept-order"),
    path("orders/ship/<uuid:uid>/", views.ship_order, name="ship-order"),
    path(
        "orders/cancel/<uuid:uid>/", views.cancel_order_item, name="cancel-order-item"
    ),
    path('orders/update/<uuid:uid>/<str:status>/', views.update_order_status, name='seller-update-order'),
]
