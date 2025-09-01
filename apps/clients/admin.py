from django.contrib import admin
from .models import Client, ClientContact


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'email', 'phone', 'client_type', 'status', 'assigned_to', 'created_at']
    list_filter = ['client_type', 'status', 'industry', 'assigned_to', 'created_at']
    search_fields = ['name', 'company_name', 'email', 'phone', 'address']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'assigned_to']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company_name', 'client_type', 'status')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Business Information', {
            'fields': ('industry', 'website', 'linkedin', 'source')
        }),
        ('Additional Information', {
            'fields': ('notes', 'assigned_to'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'position', 'email', 'phone', 'is_primary']
    list_filter = ['is_primary', 'client']
    search_fields = ['name', 'email', 'client__name']
