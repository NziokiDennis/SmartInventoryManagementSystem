from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Role(models.Model):
    ROLE_CHOICES = [
        ('store_manager', 'Store Manager'),
        ('inventory_clerk', 'Inventory Clerk'),
        ('supplier', 'Supplier'),
        ('system_admin', 'System Admin'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    # Adding related_name to avoid clashes with the built-in auth User model
    groups = models.ManyToManyField(
        Group,
        related_name='inventory_user_set',
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='inventory_user_set_permissions',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    reorder_point = models.IntegerField()
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_information = models.TextField()
    reliability_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
