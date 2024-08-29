# inventory/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Product, Order, Supplier

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Custom UserAdmin to include the role field
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock', 'reorder_point', 'supplier')
    search_fields = ('name',)
    list_filter = ('supplier',)
    ordering = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order_date', 'status')
    search_fields = ('product__name',)
    list_filter = ('status', 'order_date')
    ordering = ('-order_date',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_information', 'reliability_score')
    search_fields = ('name',)
    ordering = ('name',)
