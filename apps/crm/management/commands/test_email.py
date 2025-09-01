from django.core.management.base import BaseCommand
from django.conf import settings
from apps.crm.utils import test_email_configuration, send_crm_notification


class Command(BaseCommand):
    help = 'Test email configuration and send test emails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recipient',
            type=str,
            help='Email address to send test email to',
            default='test@example.com'
        )
        parser.add_argument(
            '--config-only',
            action='store_true',
            help='Only test configuration without sending email'
        )

    def handle(self, *args, **options):
        recipient = options['recipient']
        config_only = options['config_only']

        self.stdout.write(
            self.style.SUCCESS('Testing CRM Email Configuration...')
        )

        # Display current email settings
        self.stdout.write('\nCurrent Email Settings:')
        self.stdout.write(f'  EMAIL_BACKEND: {getattr(settings, "EMAIL_BACKEND", "Not set")}')
        self.stdout.write(f'  EMAIL_HOST: {getattr(settings, "EMAIL_HOST", "Not set")}')
        self.stdout.write(f'  EMAIL_PORT: {getattr(settings, "EMAIL_PORT", "Not set")}')
        self.stdout.write(f'  EMAIL_USE_TLS: {getattr(settings, "EMAIL_USE_TLS", "Not set")}')
        self.stdout.write(f'  EMAIL_USE_SSL: {getattr(settings, "EMAIL_USE_SSL", "Not set")}')
        self.stdout.write(f'  EMAIL_HOST_USER: {getattr(settings, "EMAIL_HOST_USER", "Not set")}')
        self.stdout.write(f'  DEFAULT_FROM_EMAIL: {getattr(settings, "DEFAULT_FROM_EMAIL", "Not set")}')

        if config_only:
            self.stdout.write(
                self.style.WARNING('\nConfiguration test completed. Use --recipient to send test email.')
            )
            return

        # Test email configuration
        self.stdout.write('\nTesting email configuration...')
        if test_email_configuration():
            self.stdout.write(
                self.style.SUCCESS('✓ Email configuration test successful!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('✗ Email configuration test failed!')
            )

        # Send test email
        self.stdout.write(f'\nSending test email to {recipient}...')
        
        try:
            result = send_crm_notification(
                subject="CRM Email Test",
                message="This is a test email to verify your SMTP configuration is working correctly.",
                recipient_list=[recipient]
            )
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Test email sent successfully to {recipient}!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to send test email to {recipient}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error sending test email: {str(e)}')
            )

        self.stdout.write('\nEmail testing completed!')

