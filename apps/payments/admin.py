from django.contrib import admin
from .models import Payment, Invoice


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['project', 'client', 'amount', 'amount_paid', 'status', 'payment_date', 'due_date', 'is_overdue']
    list_filter = ['status', 'payment_method', 'client', 'payment_date']
    search_fields = ['invoice_number', 'project__title', 'client__name']
    date_hierarchy = 'payment_date'
    list_editable = ['status', 'amount_paid']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('project', 'client', 'amount', 'amount_paid', 'status')
        }),
        ('Dates', {
            'fields': ('payment_date', 'due_date')
        }),
        ('Additional Details', {
            'fields': ('payment_method', 'invoice_number', 'description', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['is_overdue']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'payment', 'issue_date', 'due_date', 'total_amount', 'grand_total']
    list_filter = ['issue_date', 'due_date']
    search_fields = ['invoice_number', 'payment__project__title']
    date_hierarchy = 'issue_date'
