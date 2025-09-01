from django.db import models
from django.contrib.auth.models import User


class CustomSMTPConfig(models.Model):
    """Custom SMTP configuration model for user-defined email settings"""
    
    name = models.CharField(max_length=100, help_text="Configuration name (e.g., Gmail, Outlook)")
    smtp_host = models.CharField(max_length=255, help_text="SMTP server hostname")
    smtp_port = models.IntegerField(default=587, help_text="SMTP port number")
    username = models.CharField(max_length=255, help_text="Email username/address")
    password = models.CharField(max_length=255, help_text="Email password or app password")
    use_tls = models.BooleanField(default=True, help_text="Use TLS encryption")
    use_ssl = models.BooleanField(default=False, help_text="Use SSL encryption")
    from_email = models.CharField(max_length=255, help_text="From email address")
    is_active = models.BooleanField(default=True, help_text="Is this configuration active?")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='smtp_configs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Custom SMTP Configuration"
        verbose_name_plural = "Custom SMTP Configurations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.smtp_host}:{self.smtp_port})"
    
    def get_connection_params(self):
        """Get connection parameters for Python smtplib"""
        return {
            'host': self.smtp_host,
            'port': self.smtp_port,
            'username': self.username,
            'password': self.password,
            'use_tls': self.use_tls,
            'use_ssl': self.use_ssl,
            'from_email': self.from_email,
        }


class PaymentInstallment(models.Model):
    """Payment installment model for tracking project payments"""
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('advance', 'Advance Payment'),
        ('milestone', 'Milestone Payment'),
        ('final', 'Final Payment'),
        ('installment', 'Regular Installment'),
    ]
    
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='payment_installments')
    title = models.CharField(max_length=200, help_text="Payment description")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Payment amount")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='installment')
    due_date = models.DateField(help_text="When this payment is due")
    paid_date = models.DateField(null=True, blank=True, help_text="When this payment was actually paid")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Additional notes about this payment")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Payment Installment"
        verbose_name_plural = "Payment Installments"
        ordering = ['-due_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.get_status_display()})"
    
    @property
    def is_overdue(self):
        """Check if payment is overdue"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.status == 'pending' and self.due_date < today
    
    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if not self.is_overdue:
            return 0
        from django.utils import timezone
        today = timezone.now().date()
        return (today - self.due_date).days
    
    def mark_as_paid(self, paid_date=None):
        """Mark payment as paid"""
        from django.utils import timezone
        self.status = 'paid'
        self.paid_date = paid_date or timezone.now().date()
        self.save()
    
    def mark_as_overdue(self):
        """Mark payment as overdue"""
        if self.status == 'pending':
            self.status = 'overdue'
            self.save()


class EmailLog(models.Model):
    """Log of emails sent using custom SMTP"""
    
    STATUS_CHOICES = [
        ('sent', 'Sent Successfully'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    smtp_config = models.ForeignKey(CustomSMTPConfig, on_delete=models.CASCADE, related_name='email_logs')
    recipient = models.CharField(max_length=255, help_text="Recipient email address")
    subject = models.CharField(max_length=255, help_text="Email subject")
    message = models.TextField(help_text="Email message content")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True, help_text="Error message if failed")
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    
    class Meta:
        verbose_name = "Email Log"
        verbose_name_plural = "Email Logs"
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.subject} to {self.recipient} ({self.status})"

