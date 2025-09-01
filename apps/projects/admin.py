from django.contrib import admin
from .models import Project, ProjectRequirement


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'status', 'priority', 'assigned_to', 'start_date', 'due_date', 'budget']
    list_filter = ['status', 'priority', 'client', 'assigned_to', 'start_date']
    search_fields = ['title', 'description', 'client__name']
    date_hierarchy = 'start_date'
    list_editable = ['status', 'priority']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'client', 'assigned_to')
        }),
        ('Project Details', {
            'fields': ('status', 'priority', 'start_date', 'due_date', 'budget')
        }),
        ('Additional Information', {
            'fields': ('requirements', 'notes'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectRequirement)
class ProjectRequirementAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'project']
    search_fields = ['title', 'description', 'project__title']
