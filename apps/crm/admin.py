from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.conf import settings
from apps.clients.models import Client, ClientContact
from apps.projects.models import Project, ProjectRequirement
from .models import CustomSMTPConfig, EmailLog


# Note: Client, Project, and ProjectRequirement models are already registered 
# in their respective apps (apps.clients.admin and apps.projects.admin)
# We don't need to register them again here to avoid conflicts


@admin.register(CustomSMTPConfig)
class CustomSMTPConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'smtp_host', 'smtp_port', 'username', 'from_email', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'use_tls', 'use_ssl', 'created_at']
    search_fields = ['name', 'smtp_host', 'username', 'from_email']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active', 'created_by')
        }),
        ('SMTP Configuration', {
            'fields': ('smtp_host', 'smtp_port', 'username', 'password')
        }),
        ('Security Settings', {
            'fields': ('use_tls', 'use_ssl', 'from_email')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['subject', 'recipient', 'smtp_config', 'status', 'sent_at', 'sent_by']
    list_filter = ['status', 'smtp_config', 'sent_at']
    search_fields = ['subject', 'recipient', 'message']
    readonly_fields = ['sent_at', 'sent_by']
    
    fieldsets = (
        ('Email Details', {
            'fields': ('subject', 'recipient', 'message', 'status')
        }),
        ('Configuration', {
            'fields': ('smtp_config', 'error_message')
        }),
        ('Metadata', {
            'fields': ('sent_at', 'sent_by'),
            'classes': ('collapse',)
        }),
    )


# Simple email configuration display (no registration needed)
class EmailConfigInfo:
    """Display email configuration information in admin"""
    
    def __init__(self):
        self.email_backend = getattr(settings, 'EMAIL_BACKEND', 'Not configured')
        self.email_host = getattr(settings, 'EMAIL_HOST', 'Not configured')
        self.email_port = getattr(settings, 'EMAIL_PORT', 'Not configured')
        self.email_use_tls = getattr(settings, 'EMAIL_USE_TLS', 'Not configured')
        self.email_use_ssl = getattr(settings, 'EMAIL_USE_SSL', 'Not configured')
        self.email_host_user = getattr(settings, 'EMAIL_HOST_USER', 'Not configured')
        self.default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured')


# Note: All models are already registered in their respective apps
# No need to register them again here
