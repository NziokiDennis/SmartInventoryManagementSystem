from django.urls import path
from . import views

urlpatterns = [
    # Existing URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('', views.landing_page, name='landing_page'),
    path('visualizations/', views.product_visualization, name='product_visualization'),

    # New URLs for authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # New URLs for role-specific dashboards
    path('inventory_clerks/welcome_dashboard/', views.inventory_clerk_dashboard, name='inventory_clerk_dashboard'),
    path('suppliers/welcome_dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('system_admins/welcome_dashboard/', views.system_admin_dashboard, name='system_admin_dashboard'),
    path('store_managers/dashboard/', views.store_manager_dashboard, name='store_manager_dashboard'),
]
