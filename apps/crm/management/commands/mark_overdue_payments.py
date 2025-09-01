from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.crm.models import PaymentInstallment


class Command(BaseCommand):
    help = 'Mark overdue payment installments as overdue'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Find pending payments that are overdue
        overdue_payments = PaymentInstallment.objects.filter(
            status='pending',
            due_date__lt=today
        )
        
        count = 0
        for payment in overdue_payments:
            payment.status = 'overdue'
            payment.save()
            count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Marked "{payment.title}" (₹{payment.amount}) as overdue'
                )
            )
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No overdue payments found.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully marked {count} payment(s) as overdue.'
                )
            )
