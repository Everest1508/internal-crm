from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Client URLs
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    
    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/requirements/add/', views.requirement_add, name='requirement_add'),
    path('projects/<int:project_id>/complete/', views.project_complete, name='project_complete'),
    
    # Email testing
    path('test-email/', views.test_email_view, name='test_email'),
    
    # Custom SMTP Management
    path('smtp-configs/', views.smtp_config_list, name='smtp_config_list'),
    path('smtp-configs/create/', views.smtp_config_create, name='smtp_config_create'),
    path('smtp-configs/<int:config_id>/edit/', views.smtp_config_edit, name='smtp_config_edit'),
    path('smtp-configs/<int:config_id>/delete/', views.smtp_config_delete, name='smtp_config_delete'),
    path('smtp-configs/<int:config_id>/test/', views.test_smtp_connection, name='test_smtp_connection'),
    
    # Custom Email Sending
    path('send-email/', views.send_custom_email, name='send_custom_email'),
    path('email-logs/', views.email_logs, name='email_logs'),
    
    # Payment Installments
    path('payments/', views.payment_installment_list, name='payment_installment_list'),
    path('payments/create/', views.payment_installment_create, name='payment_installment_create'),
    path('payments/<int:installment_id>/edit/', views.payment_installment_edit, name='payment_installment_edit'),
    path('payments/<int:installment_id>/mark-paid/', views.payment_installment_mark_paid, name='payment_installment_mark_paid'),
    path('payments/<int:installment_id>/delete/', views.payment_installment_delete, name='payment_installment_delete'),
    path('project/<int:project_id>/financial-data/', views.get_project_financial_data, name='get_project_financial_data'),
    path('debug/payments/', views.debug_payments, name='debug_payments'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
