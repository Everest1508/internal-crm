from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from datetime import timedelta
from apps.clients.models import Client, ClientContact
from apps.projects.models import Project, ProjectRequirement
from .models import CustomSMTPConfig, EmailLog, PaymentInstallment


@login_required
def client_list(request):
    """Display list of clients"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    clients = Client.objects.all()
    
    # Apply search filter
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter:
        clients = clients.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'segment': 'clients',
        'clients': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'crm/clients/client_list.html', context)


@login_required
def client_detail(request, client_id):
    """Display client details"""
    client = get_object_or_404(Client, id=client_id)
    projects = client.projects.all()
    
    context = {
        'segment': 'clients',
        'client': client,
        'projects': projects,
    }
    return render(request, 'crm/clients/client_detail.html', context)


@login_required
def client_create(request):
    """Create new client"""
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        status = request.POST.get('status', 'active')
        
        client = Client.objects.create(
            name=name,
            company_name=company_name,
            email=email,
            phone=phone,
            status=status,
            assigned_to=request.user
        )
        
        messages.success(request, f'Client "{client.name}" created successfully!')
        return redirect('crm:client_detail', client_id=client.id)
    
    context = {
        'segment': 'clients',
    }
    return render(request, 'crm/clients/client_form.html', context)


@login_required
def project_list(request):
    """Display list of projects"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    projects = Project.objects.all()
    
    # Apply search filter
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(client__name__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'segment': 'projects',
        'projects': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'crm/projects/project_list.html', context)


@login_required
def project_detail(request, project_id):
    """Display project details"""
    project = get_object_or_404(Project, id=project_id)
    requirements = project.project_requirements.all()
    
    context = {
        'segment': 'projects',
        'project': project,
        'requirements': requirements,
    }
    return render(request, 'crm/projects/project_detail.html', context)


@login_required
def project_create(request):
    """Create new project"""
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        client_id = request.POST.get('client')
        start_date = request.POST.get('start_date')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status', 'not_started')
        priority = request.POST.get('priority', 'medium')
        
        client = None
        if client_id:
            client = Client.objects.get(id=client_id)
        
        project = Project.objects.create(
            title=title,
            description=description,
            client=client,
            start_date=start_date,
            due_date=due_date,
            status=status,
            priority=priority,
            budget=request.POST.get('budget') or None,
            assigned_to=request.user
        )
        
        messages.success(request, f'Project "{project.title}" created successfully!')
        return redirect('crm:project_detail', project_id=project.id)
    
    clients = Client.objects.all()
    context = {
        'segment': 'projects',
        'clients': clients,
    }
    return render(request, 'crm/projects/project_form.html', context)


@login_required
def project_edit(request, project_id):
    """Edit existing project"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        # Handle form submission
        client_id = request.POST.get('client')
        client = None
        if client_id:
            client = Client.objects.get(id=client_id)
        
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.client = client
        project.start_date = request.POST.get('start_date')
        project.due_date = request.POST.get('due_date')
        project.status = request.POST.get('status')
        project.priority = request.POST.get('priority')
        project.budget = request.POST.get('budget') or None
        
        if client_id:
            project.save()
            messages.success(request, f'Project "{project.title}" updated successfully!')
            return redirect('crm:project_detail', project_id=project.id)
    
    clients = Client.objects.all()
    context = {
        'segment': 'projects',
        'project': project,
        'clients': clients,
    }
    return render(request, 'crm/projects/project_form.html', context)


@login_required
def requirement_add(request, project_id):
    """Add new requirement to project"""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)
        requirement = ProjectRequirement.objects.create(
            project=project,
            title=title,
            description=description,
            is_completed=is_completed
        )
        messages.success(request, f'Requirement "{requirement.title}" added successfully!')
        return redirect('crm:project_detail', project_id=project.id)
    context = { 'segment': 'projects', 'project': project, }
    return render(request, 'crm/projects/requirement_form.html', context)


@login_required
def project_complete(request, project_id):
    """Mark project as complete"""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.status = 'completed'
        project.save()
        messages.success(request, f'Project "{project.title}" marked as completed!')
        return redirect('crm:project_detail', project_id=project.id)
    context = { 'segment': 'projects', 'project': project, }
    return render(request, 'crm/projects/project_complete_confirm.html', context)


@login_required
def test_email_view(request):
    """Test email configuration"""
    if request.method == 'POST':
        try:
            from .custom_email import send_custom_email
            
            recipient = request.POST.get('recipient_email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            if not all([recipient, subject, message]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('crm:test_email')
            
            # Send email
            success = send_custom_email(
                recipient=recipient,
                subject=subject,
                message=message,
                user=request.user
            )
            
            if success:
                messages.success(request, f'Test email sent successfully to {recipient}!')
            else:
                messages.error(request, 'Failed to send test email. Check the logs for details.')
                
        except Exception as e:
            messages.error(request, f'Error sending test email: {str(e)}')
    
    context = {
        'segment': 'email_test',
    }
    return render(request, 'crm/email_test.html', context)


# Payment Installment Views
@login_required
def payment_installment_list(request):
    """List all payment installments"""
    installments = PaymentInstallment.objects.select_related('project', 'project__client').order_by('-due_date')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        installments = installments.filter(status=status_filter)
    
    # Filter by project if provided
    project_filter = request.GET.get('project')
    if project_filter:
        installments = installments.filter(project_id=project_filter)
    
    context = {
        'segment': 'payment_installments',
        'installments': installments,
        'projects': Project.objects.all(),
        'status_choices': PaymentInstallment.PAYMENT_STATUS_CHOICES,
        'today': timezone.now().date(),
    }
    return render(request, 'crm/payments/installment_list.html', context)


@login_required
def payment_installment_create(request):
    """Create new payment installment with smart validation"""
    if request.method == 'POST':
        try:
            project_id = request.POST.get('project')
            title = request.POST.get('title')
            amount = float(request.POST.get('amount'))
            payment_type = request.POST.get('payment_type')
            due_date = request.POST.get('due_date')
            notes = request.POST.get('notes', '')
            
            project = Project.objects.get(id=project_id)
            
            # Calculate remaining amount
            total_paid = PaymentInstallment.objects.filter(
                project=project, 
                status='paid'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            remaining_amount = (project.budget or 0) - total_paid
            
            # Validate amount doesn't exceed remaining budget
            if amount > remaining_amount:
                messages.error(request, f'Amount ₹{amount} exceeds remaining budget ₹{remaining_amount}. Please enter a smaller amount.')
                context = {
                    'segment': 'payment_installments',
                    'projects': Project.objects.all(),
                    'payment_types': PaymentInstallment.PAYMENT_TYPE_CHOICES,
                    'selected_project': project,
                    'project_budget': project.budget or 0,
                    'total_paid': total_paid,
                    'remaining_amount': remaining_amount,
                    'entered_amount': amount,
                }
                return render(request, 'crm/payments/installment_form.html', context)
            
            installment = PaymentInstallment.objects.create(
                project_id=project_id,
                title=title,
                amount=amount,
                payment_type=payment_type,
                due_date=due_date,
                notes=notes,
                created_by=request.user
            )
            
            messages.success(request, f'Payment installment "{installment.title}" created successfully!')
            return redirect('crm:payment_installment_list')
            
        except Exception as e:
            messages.error(request, f'Failed to create payment installment: {str(e)}')
    
    # Check if project is pre-selected from project detail page
    selected_project_id = request.GET.get('project')
    selected_project = None
    if selected_project_id:
        try:
            selected_project = Project.objects.get(id=selected_project_id)
        except Project.DoesNotExist:
            pass
    
    context = {
        'segment': 'payment_installments',
        'projects': Project.objects.all(),
        'payment_types': PaymentInstallment.PAYMENT_TYPE_CHOICES,
        'selected_project': selected_project,
    }
    return render(request, 'crm/payments/installment_form.html', context)


@login_required
def get_project_financial_data(request, project_id):
    """Get project financial data for AJAX requests"""
    try:
        project = Project.objects.get(id=project_id)
        
        # Calculate financial data
        total_paid = PaymentInstallment.objects.filter(
            project=project, 
            status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        remaining_amount = (project.budget or 0) - total_paid
        
        data = {
            'budget': float(project.budget or 0),
            'total_paid': float(total_paid),
            'remaining_amount': float(remaining_amount),
            'max_amount': float(remaining_amount),
        }
        
        return JsonResponse(data)
        
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def payment_installment_edit(request, installment_id):
    """Edit existing payment installment"""
    installment = get_object_or_404(PaymentInstallment, id=installment_id)
    
    if request.method == 'POST':
        try:
            installment.project_id = request.POST.get('project')
            installment.title = request.POST.get('title')
            installment.amount = request.POST.get('amount')
            installment.payment_type = request.POST.get('payment_type')
            installment.due_date = request.POST.get('due_date')
            installment.notes = request.POST.get('notes')
            installment.save()
            
            messages.success(request, f'Payment installment "{installment.title}" updated successfully!')
            return redirect('crm:payment_installment_list')
            
        except Exception as e:
            messages.error(request, f'Failed to update payment installment: {str(e)}')
    
    context = {
        'segment': 'payment_installments',
        'installment': installment,
        'projects': Project.objects.all(),
        'payment_types': PaymentInstallment.PAYMENT_TYPE_CHOICES,
    }
    return render(request, 'crm/payments/installment_form.html', context)


@login_required
def payment_installment_mark_paid(request, installment_id):
    """Mark payment installment as paid"""
    installment = get_object_or_404(PaymentInstallment, id=installment_id)
    
    if request.method == 'POST':
        try:
            paid_date = request.POST.get('paid_date')
            if not paid_date:
                paid_date = timezone.now().date()
            
            # Update the installment
            installment.status = 'paid'
            installment.paid_date = paid_date
            installment.save()
            
            messages.success(request, f'Payment "{installment.title}" marked as paid!')
            return redirect('crm:payment_installment_list')
            
        except Exception as e:
            messages.error(request, f'Failed to mark payment as paid: {str(e)}')
    
    # Show form for marking as paid
    context = {
        'segment': 'payment_installments',
        'installment': installment,
        'today': timezone.now().date(),
    }
    return render(request, 'crm/payments/mark_paid_form.html', context)


@login_required
def debug_payments(request):
    """Debug view to check payment installments in database"""
    all_installments = PaymentInstallment.objects.all()
    paid_installments = PaymentInstallment.objects.filter(status='paid')
    pending_installments = PaymentInstallment.objects.filter(status='pending')
    
    # Calculate totals
    total_paid = paid_installments.aggregate(total=Sum('amount'))['total'] or 0
    total_pending = pending_installments.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'all_installments': all_installments,
        'paid_installments': paid_installments,
        'pending_installments': pending_installments,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_count': all_installments.count(),
        'paid_count': paid_installments.count(),
        'pending_count': pending_installments.count(),
    }
    
    return render(request, 'crm/debug_payments.html', context)


@login_required
def payment_installment_delete(request, installment_id):
    """Delete payment installment"""
    installment = get_object_or_404(PaymentInstallment, id=installment_id)
    
    if request.method == 'POST':
        installment_title = installment.title
        installment.delete()
        messages.success(request, f'Payment installment "{installment_title}" deleted successfully!')
        return redirect('crm:payment_installment_list')
    
    context = {
        'segment': 'payment_installments',
        'installment': installment,
    }
    return render(request, 'crm/payments/installment_confirm_delete.html', context)


def get_dashboard_stats():
    """Get dashboard statistics including total income from all paid installments"""
    from django.utils import timezone
    from django.db.models import Sum, Count, Q
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Debug: Check all payment installments
    all_installments = PaymentInstallment.objects.all()
    paid_installments = PaymentInstallment.objects.filter(status='paid')
    
    # Total income from ALL paid installments (not just monthly)
    total_income = paid_installments.aggregate(total=Sum('amount'))['total'] or 0
    
    # Monthly income from paid installments
    monthly_income = PaymentInstallment.objects.filter(
        status='paid',
        paid_date__gte=current_month_start,
        paid_date__lte=current_month_end
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Total pending payments
    pending_payments = PaymentInstallment.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Overdue payments
    overdue_payments = PaymentInstallment.objects.filter(
        Q(status='pending') & Q(due_date__lt=today)
    ).aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    # Project statistics
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status__in=['in_progress', 'on_hold']).count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    # Client statistics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(
        projects__status__in=['in_progress', 'on_hold']
    ).distinct().count()
    
    # Debug: Print to console (will show in Django logs)
    print(f"DEBUG: Total installments: {all_installments.count()}")
    print(f"DEBUG: Paid installments: {paid_installments.count()}")
    print(f"DEBUG: Total income: {total_income}")
    print(f"DEBUG: Monthly income: {monthly_income}")
    
    return {
        'total_income': total_income,
        'monthly_income': monthly_income,
        'pending_payments': pending_payments,
        'overdue_payments_total': overdue_payments['total'] or 0,
        'overdue_payments_count': overdue_payments['count'] or 0,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_clients': total_clients,
        'active_clients': active_clients,
    }


@login_required
def dashboard_view(request):
    """Custom dashboard view with payment statistics"""
    stats = get_dashboard_stats()
    
    # Recent projects
    recent_projects = Project.objects.select_related('client').order_by('-created_at')[:5]
    
    # Recent payments
    recent_payments = PaymentInstallment.objects.select_related('project', 'project__client').order_by('-paid_date')[:5]
    
    # Upcoming payments
    from django.utils import timezone
    today = timezone.now().date()
    upcoming_payments = PaymentInstallment.objects.filter(
        status='pending',
        due_date__gte=today
    ).select_related('project', 'project__client').order_by('due_date')[:5]
    
    # Generate monthly income data for chart
    monthly_income_data = []
    month_labels = []
    
    for i in range(6):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_income = PaymentInstallment.objects.filter(
            status='paid',
            paid_date__gte=month_start,
            paid_date__lte=month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_income_data.append(float(month_income))
        month_labels.append(month_date.strftime('%b'))
    
    # Reverse to show oldest to newest
    monthly_income_data.reverse()
    month_labels.reverse()
    
    context = {
        'segment': 'dashboard',
        'total_clients': stats['total_clients'],
        'total_projects': stats['total_projects'],
        'total_income': stats['total_income'],  # Total income from all paid installments
        'pending_projects': stats['total_projects'] - stats['completed_projects'],
        'completed_projects': stats['completed_projects'],
        'in_progress_projects': stats['active_projects'],
        'recent_projects': recent_projects,
        'recent_payments': recent_payments,
        'upcoming_payments': upcoming_payments,
        'monthly_income': monthly_income_data,
        'month_labels': month_labels,
        'today': today,
    }
    return render(request, 'pages/index.html', context)


# SMTP Configuration Views
@login_required
def smtp_config_list(request):
    """List all custom SMTP configurations"""
    configs = CustomSMTPConfig.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'segment': 'smtp_configs',
        'configs': configs,
    }
    return render(request, 'crm/smtp_config_list.html', context)


@login_required
def smtp_config_create(request):
    """Create new custom SMTP configuration"""
    if request.method == 'POST':
        try:
            config = CustomSMTPConfig.objects.create(
                name=request.POST.get('name'),
                smtp_host=request.POST.get('smtp_host'),
                smtp_port=int(request.POST.get('smtp_port', 587)),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                use_tls=request.POST.get('use_tls') == 'on',
                use_ssl=request.POST.get('use_ssl') == 'on',
                from_email=request.POST.get('from_email'),
                is_active=request.POST.get('is_active') == 'on',
                created_by=request.user
            )
            
            messages.success(request, f'SMTP configuration "{config.name}" created successfully!')
            return redirect('crm:smtp_config_list')
            
        except Exception as e:
            messages.error(request, f'Failed to create SMTP configuration: {str(e)}')
    
    context = {
        'segment': 'smtp_configs',
    }
    return render(request, 'crm/smtp_config_form.html', context)


@login_required
def smtp_config_edit(request, config_id):
    """Edit existing SMTP configuration"""
    config = get_object_or_404(CustomSMTPConfig, id=config_id, created_by=request.user)
    
    if request.method == 'POST':
        try:
            config.name = request.POST.get('name')
            config.smtp_host = request.POST.get('smtp_host')
            config.smtp_port = int(request.POST.get('smtp_port', 587))
            config.username = request.POST.get('username')
            config.password = request.POST.get('password')
            config.use_tls = request.POST.get('use_tls') == 'on'
            config.use_ssl = request.POST.get('use_ssl') == 'on'
            config.from_email = request.POST.get('from_email')
            config.is_active = request.POST.get('is_active') == 'on'
            config.save()
            
            messages.success(request, f'SMTP configuration "{config.name}" updated successfully!')
            return redirect('crm:smtp_config_list')
            
        except Exception as e:
            messages.error(request, f'Failed to update SMTP configuration: {str(e)}')
    
    context = {
        'segment': 'smtp_configs',
        'config': config,
    }
    return render(request, 'crm/smtp_config_form.html', context)


@login_required
def smtp_config_delete(request, config_id):
    """Delete SMTP configuration"""
    config = get_object_or_404(CustomSMTPConfig, id=config_id, created_by=request.user)
    
    if request.method == 'POST':
        config_name = config.name
        config.delete()
        messages.success(request, f'SMTP configuration "{config_name}" deleted successfully!')
        return redirect('crm:smtp_config_list')
    
    context = {
        'segment': 'smtp_configs',
        'config': config,
    }
    return render(request, 'crm/smtp_config_confirm_delete.html', context)


@login_required
def test_smtp_connection(request, config_id):
    """Test SMTP connection"""
    config = get_object_or_404(CustomSMTPConfig, id=config_id, created_by=request.user)
    
    try:
        from .custom_email import test_smtp_connection
        success, message = test_smtp_connection(config_id)
        
        if success:
            messages.success(request, f'Connection test successful: {message}')
        else:
            messages.error(request, f'Connection test failed: {message}')
            
    except Exception as e:
        messages.error(request, f'Connection test error: {str(e)}')
    
    return redirect('crm:smtp_config_list')


@login_required
def send_custom_email(request):
    """Send email using custom SMTP configuration"""
    if request.method == 'POST':
        try:
            from .custom_email import send_custom_email
            
            recipient = request.POST.get('recipient_email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            html_message = request.POST.get('html_message')
            smtp_config_id = request.POST.get('smtp_config')
            
            if not all([recipient, subject, message]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('crm:send_custom_email')
            
            # Send email
            success = send_custom_email(
                recipient=recipient,
                subject=subject,
                message=message,
                html_message=html_message,
                smtp_config_id=smtp_config_id,
                user=request.user
            )
            
            if success:
                messages.success(request, f'Email sent successfully to {recipient}!')
            else:
                messages.error(request, 'Failed to send email. Check the logs for details.')
                
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
    
    # Get available SMTP configurations
    configs = CustomSMTPConfig.objects.filter(created_by=request.user, is_active=True)
    
    context = {
        'segment': 'send_custom_email',
        'configs': configs,
    }
    return render(request, 'crm/send_custom_email.html', context)


@login_required
def email_logs(request):
    """View email logs"""
    logs = EmailLog.objects.filter(smtp_config__created_by=request.user).order_by('-sent_at')[:100]
    
    context = {
        'segment': 'email_logs',
        'logs': logs,
    }
    return render(request, 'crm/email_logs.html', context)
