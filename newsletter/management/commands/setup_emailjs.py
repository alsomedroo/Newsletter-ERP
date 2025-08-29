from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Setup EmailJS credentials for the newsletter application'

    def add_arguments(self, parser):
        parser.add_argument('--service-id', type=str, help='EmailJS Service ID')
        parser.add_argument('--template-id', type=str, help='EmailJS Template ID')
        parser.add_argument('--public-key', type=str, help='EmailJS Public Key')

    def handle(self, *args, **options):
        service_id = options.get('service_id')
        template_id = options.get('template_id')
        public_key = options.get('public_key')

        if not service_id:
            service_id = input('Enter EmailJS Service ID: ')
        
        if not template_id:
            template_id = input('Enter EmailJS Template ID: ')
        
        if not public_key:
            public_key = input('Enter EmailJS Public Key: ')

        # Path to .env file
        env_file = os.path.join(settings.BASE_DIR, '.env')
        
        # Read existing .env file
        env_lines = []
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_lines = f.readlines()

        # Update or add EmailJS settings
        updated_lines = []
        service_updated = False
        template_updated = False
        key_updated = False

        for line in env_lines:
            if line.startswith('EMAILJS_SERVICE_ID='):
                updated_lines.append(f'EMAILJS_SERVICE_ID={service_id}\n')
                service_updated = True
            elif line.startswith('EMAILJS_TEMPLATE_ID='):
                updated_lines.append(f'EMAILJS_TEMPLATE_ID={template_id}\n')
                template_updated = True
            elif line.startswith('EMAILJS_PUBLIC_KEY='):
                updated_lines.append(f'EMAILJS_PUBLIC_KEY={public_key}\n')
                key_updated = True
            else:
                updated_lines.append(line)

        # Add missing settings
        if not service_updated:
            updated_lines.append(f'EMAILJS_SERVICE_ID={service_id}\n')
        if not template_updated:
            updated_lines.append(f'EMAILJS_TEMPLATE_ID={template_id}\n')
        if not key_updated:
            updated_lines.append(f'EMAILJS_PUBLIC_KEY={public_key}\n')

        # Write back to .env file
        with open(env_file, 'w') as f:
            f.writelines(updated_lines)

        self.stdout.write(
            self.style.SUCCESS('EmailJS credentials have been saved to .env file!')
        )
        self.stdout.write(
            self.style.SUCCESS('Please restart the Django server for changes to take effect.')
        )
        self.stdout.write(
            self.style.WARNING('Note: Make sure to add .env to your .gitignore file to keep credentials secure.')
        )