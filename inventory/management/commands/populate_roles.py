# inventory/management/commands/populate_roles.py

from django.core.management.base import BaseCommand
from inventory.models import Role

class Command(BaseCommand):
    help = 'Create initial roles in the database'

    def handle(self, *args, **kwargs):
        roles = [
            'store_manager',
            'inventory_clerk',
            'supplier',
            'system_admin'
        ]
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)
        self.stdout.write(self.style.SUCCESS('Successfully created initial roles'))
