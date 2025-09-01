from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PaymentInstallment


@receiver(pre_save, sender=PaymentInstallment)
def update_payment_status(sender, instance, **kwargs):
    """Update payment status based on due date and paid status"""
    today = timezone.now().date()
    
    # If payment is marked as paid, ensure paid_date is set
    if instance.status == 'paid' and not instance.paid_date:
        instance.paid_date = today
    
    # If payment is pending and due date is in the past, mark as overdue
    if instance.status == 'pending' and instance.due_date < today:
        instance.status = 'overdue'
    
    # If payment is overdue but due date is in the future, mark as pending
    if instance.status == 'overdue' and instance.due_date >= today:
        instance.status = 'pending'


@receiver(post_save, sender=PaymentInstallment)
def log_payment_status_change(sender, instance, created, **kwargs):
    """Log when payment status changes"""
    if created:
        print(f"Created payment installment: {instance.title} - Status: {instance.status}")
    else:
        print(f"Updated payment installment: {instance.title} - Status: {instance.status}")
