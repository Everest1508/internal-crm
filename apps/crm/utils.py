from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def send_crm_notification(subject, message, recipient_list, from_email=None, html_message=None):
    """
    Send a CRM notification email
    
    Args:
        subject (str): Email subject
        message (str): Plain text message
        recipient_list (list): List of email addresses
        from_email (str): From email address (uses DEFAULT_FROM_EMAIL if None)
        html_message (str): HTML version of the message
    """
    try:
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
            
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Email sent successfully to {recipient_list}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {str(e)}")
        return False


def send_project_update_notification(project, update_type, recipients=None):
    """
    Send project update notification emails
    
    Args:
        project: Project instance
        update_type (str): Type of update (created, updated, completed, etc.)
        recipients (list): List of email addresses (uses project team if None)
    """
    if recipients is None:
        recipients = []
        if project.assigned_to and project.assigned_to.email:
            recipients.append(project.assigned_to.email)
        if project.client.email:
            recipients.append(project.client.email)
    
    if not recipients:
        return False
    
    subject = f"Project Update: {project.title}"
    
    # Create context for email templates
    context = {
        'project': project,
        'update_type': update_type,
        'project_url': f"{settings.SITE_URL}/crm/projects/{project.id}/" if hasattr(settings, 'SITE_URL') else f"/crm/projects/{project.id}/"
    }
    
    # Plain text message
    message = render_to_string('crm/emails/project_update.txt', context)
    
    # HTML message
    html_message = render_to_string('crm/emails/project_update.html', context)
    
    return send_crm_notification(subject, message, recipients, html_message=html_message)


def send_client_welcome_email(client):
    """
    Send welcome email to new client
    
    Args:
        client: Client instance
    """
    if not client.email:
        return False
    
    subject = f"Welcome to {client.company_name or 'our services'}!"
    
    context = {
        'client': client,
        'site_name': 'CRM System'
    }
    
    message = render_to_string('crm/emails/client_welcome.txt', context)
    html_message = render_to_string('crm/emails/client_welcome.html', context)
    
    return send_crm_notification(subject, message, [client.email], html_message=html_message)


def send_project_reminder_emails():
    """
    Send reminder emails for upcoming project deadlines
    This can be called by a management command or cron job
    """
    from django.utils import timezone
    from datetime import timedelta
    from apps.projects.models import Project
    
    # Get projects due in the next 3 days
    upcoming_deadline = timezone.now().date() + timedelta(days=3)
    projects = Project.objects.filter(
        due_date__lte=upcoming_deadline,
        status__in=['planning', 'in_progress'],
        assigned_to__isnull=False
    )
    
    for project in projects:
        if project.assigned_to and project.assigned_to.email:
            days_until_due = (project.due_date - timezone.now().date()).days
            
            subject = f"Project Deadline Reminder: {project.title}"
            
            context = {
                'project': project,
                'days_until_due': days_until_due,
                'project_url': f"{settings.SITE_URL}/crm/projects/{project.id}/" if hasattr(settings, 'SITE_URL') else f"/crm/projects/{project.id}/"
            }
            
            message = render_to_string('crm/emails/project_reminder.txt', context)
            html_message = render_to_string('crm/emails/project_reminder.html', context)
            
            send_crm_notification(subject, message, [project.assigned_to.email], html_message=html_message)


def send_mass_project_notifications(projects, notification_type, recipients):
    """
    Send mass notifications for multiple projects
    
    Args:
        projects: QuerySet of projects
        notification_type (str): Type of notification
        recipients (list): List of email addresses
    """
    if not projects or not recipients:
        return False
    
    subject = f"Project {notification_type.title()} - {len(projects)} projects"
    
    # Create a summary message
    project_list = "\n".join([f"- {p.title} ({p.client.name})" for p in projects])
    
    message = f"""
    Project {notification_type.title()} Summary
    
    The following projects have been {notification_type}:
    
    {project_list}
    
    Please review and take necessary actions.
    """
    
    return send_crm_notification(subject, message, recipients)


def test_email_configuration():
    """
    Test email configuration by sending a test email
    """
    try:
        test_subject = "CRM Email Test"
        test_message = "This is a test email to verify your SMTP configuration is working correctly."
        
        # Send to a test recipient (you can change this)
        test_recipient = ['test@example.com']
        
        result = send_crm_notification(test_subject, test_message, test_recipient)
        
        if result:
            logger.info("Email configuration test successful")
            return True
        else:
            logger.error("Email configuration test failed")
            return False
            
    except Exception as e:
        logger.error(f"Email configuration test error: {str(e)}")
        return False

