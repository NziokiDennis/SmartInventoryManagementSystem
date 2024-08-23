from django.core.management.base import BaseCommand
from inventory.models import Product

class Command(BaseCommand):
    help = 'Replenish stock based on reorder point'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            if product.stock < product.reorder_point:
                # Replenish stock logic (for example, adding 10 units)
                product.stock += 10
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Replenished {product.name} to {product.stock} units.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{product.name} is at sufficient stock.'))
