from django.urls import path
from . import views
from .views import register, login, logout

urlpatterns = [
    # Existing URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('visualizations/', views.product_visualization, name='product_visualization'),

    # New URLs for authentication
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
