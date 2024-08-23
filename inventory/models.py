from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    reorder_point = models.IntegerField()
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)  # Add this line

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
