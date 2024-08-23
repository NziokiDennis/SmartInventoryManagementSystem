from django.core.management.base import BaseCommand
from inventory.models import Product, Order, Supplier
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Product.objects.all().delete()
        Order.objects.all().delete()
        Supplier.objects.all().delete()

        fake = Faker()

        # Create suppliers
        suppliers = []
        for _ in range(10):  # Adjust the number of suppliers as needed
            suppliers.append(Supplier.objects.create(
                name=fake.company(),
                contact_information=fake.email(),
                reliability_score=round(random.uniform(50.0, 100.0), 2)
            ))

        # Create products
        products = []
        for _ in range(50):  # Adjust the number of products as needed
            supplier = random.choice(suppliers)
            products.append(Product.objects.create(
                name=fake.word().capitalize() + ' ' + fake.word().capitalize(),
                description=fake.sentence(),
                price=round(random.uniform(5.0, 100.0), 2),
                stock=random.randint(1, 100),
                reorder_point=random.randint(1, 20),
                supplier=supplier
            ))

        # Create orders
        for _ in range(50):  # Adjust the number of orders as needed
            Order.objects.create(
                product=random.choice(products),
                quantity=random.randint(1, 20),
                order_date=fake.date_time_this_year(),
                status=random.choice(['Pending', 'Shipped', 'Delivered'])
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
