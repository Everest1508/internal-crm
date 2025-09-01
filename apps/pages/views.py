from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
from apps.clients.models import Client
from apps.projects.models import Project

# Create your views here.

def index(request):
    # Get current date for calculations
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    # Calculate statistics
    total_clients = Client.objects.count()
    total_projects = Project.objects.count()
    
    # Get projects by status (using actual status choices from model)
    completed_projects = Project.objects.filter(status='completed').count()
    in_progress_projects = Project.objects.filter(status='in_progress').count()
    pending_projects = Project.objects.filter(status='planning').count()
    on_hold_projects = Project.objects.filter(status='on_hold').count()
    
    # Calculate percentages for progress bars
    total_active_projects = completed_projects + in_progress_projects + pending_projects + on_hold_projects
    if total_active_projects > 0:
        completed_percentage = int((completed_projects / total_active_projects) * 100)
        in_progress_percentage = int((in_progress_projects / total_active_projects) * 100)
        pending_percentage = int((pending_projects / total_active_projects) * 100)
    else:
        completed_percentage = 0
        in_progress_percentage = 0
        pending_percentage = 0
    
    # Calculate total income based on actual project budgets
    total_income = Project.objects.aggregate(
        total_budget=Sum('budget')
    )['total_budget'] or 0
    
    # Get recent projects (last 5)
    recent_projects = Project.objects.select_related('client').order_by('-created_at')[:5]
    
    # Calculate monthly income for chart based on actual data
    monthly_income = []
    month_labels = []
    
    for i in range(6):
        month_date = now - timedelta(days=30*i)
        month_income = Project.objects.filter(
            created_at__month=month_date.month,
            created_at__year=month_date.year
        ).aggregate(
            month_budget=Sum('budget')
        )['month_budget'] or 0
        
        monthly_income.append(float(month_income))
        month_labels.append(month_date.strftime('%b'))
    
    monthly_income.reverse()  # Show oldest to newest
    month_labels.reverse()
    
    context = {
        'segment': 'dashboard',
        'total_clients': total_clients,
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'in_progress_projects': in_progress_projects,
        'pending_projects': pending_projects,
        'on_hold_projects': on_hold_projects,
        'completed_percentage': completed_percentage,
        'in_progress_percentage': in_progress_percentage,
        'pending_percentage': pending_percentage,
        'total_income': total_income,
        'recent_projects': recent_projects,
        'monthly_income': monthly_income,
        'month_labels': month_labels,
    }
    
    # Page from the theme 
    return render(request, 'pages/index.html', context)
