from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import getpass

class Command(BaseCommand):
    help = 'Create a superuser admin for the newsletter application'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')

        if not username:
            username = input('Username: ')
        
        if not email:
            email = input('Email: ')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User "{username}" already exists!')
            )
            return

        password = getpass.getpass('Password: ')
        password2 = getpass.getpass('Password (again): ')

        if password != password2:
            self.stdout.write(
                self.style.ERROR('Passwords do not match!')
            )
            return

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Admin user "{username}" created successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'You can now login at: http://localhost:8000/admin/')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )