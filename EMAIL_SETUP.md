# CRM Email Configuration Guide

This guide explains how to configure email functionality in your CRM system.

## 📧 Email Backends

### 1. Console Backend (Development)
For development and testing, emails are printed to the console:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 2. File Backend (Development)
Save emails as files for testing:
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')
```

### 3. SMTP Backend (Production)
For production use with real email delivery:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

## 🔧 SMTP Configuration

### Gmail SMTP
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
```

### Outlook/Hotmail SMTP
```python
EMAIL_HOST = 'smtp.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Yahoo SMTP
```python
EMAIL_HOST = 'smtp.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yahoo.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Zoho SMTP
```python
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@zoho.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### SendGrid SMTP
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

### Mailgun SMTP
```python
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@yourdomain.mailgun.org'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
```

## 🚀 Quick Setup Steps

### Step 1: Choose Your Email Provider
1. **Gmail**: Good for personal/small business use
2. **Outlook**: Good for business accounts
3. **SendGrid**: Excellent for high-volume sending
4. **Mailgun**: Great for transactional emails

### Step 2: Configure Settings
Edit `config/settings.py` and uncomment the appropriate SMTP configuration:

```python
# Uncomment and configure for your email provider
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change to your provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Step 3: Test Configuration
Run the test command:
```bash
python manage.py test_email --recipient your-email@domain.com
```

### Step 4: Update From Email
Set your sender email:
```python
DEFAULT_FROM_EMAIL = 'Your Company <noreply@yourdomain.com>'
SERVER_EMAIL = 'server@yourdomain.com'
```

## 🔐 Security Best Practices

### 1. Use Environment Variables
Never hardcode passwords in settings:
```python
import os
from decouple import config

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

### 2. Use App Passwords (Gmail)
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password instead of regular password

### 3. Use TLS Encryption
Always use TLS (port 587) instead of SSL (port 465):
```python
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

## 📱 Email Templates

The CRM system includes these email templates:
- `project_update.html` - Project status updates
- `client_welcome.html` - New client welcome emails
- `project_reminder.html` - Deadline reminders

Templates are located in: `templates/crm/emails/`

## 🧪 Testing

### Test Email Configuration
```bash
# Test configuration only
python manage.py test_email --config-only

# Test with specific recipient
python manage.py test_email --recipient test@example.com
```

### Test from Django Shell
```python
python manage.py shell

from apps.crm.utils import send_crm_notification
send_crm_notification(
    subject="Test Email",
    message="This is a test email",
    recipient_list=['test@example.com']
)
```

## 📊 Email Features

### 1. Project Notifications
- Project creation/updates
- Status changes
- Deadline reminders

### 2. Client Communications
- Welcome emails
- Project updates
- Status notifications

### 3. Team Notifications
- Assignment notifications
- Progress updates
- Deadline alerts

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Failed
- Check username/password
- Use App Password for Gmail
- Verify account settings

#### 2. Connection Refused
- Check firewall settings
- Verify SMTP port
- Check provider status

#### 3. TLS/SSL Issues
- Use port 587 with TLS
- Avoid port 465 with SSL
- Check provider requirements

### Debug Mode
Enable debug logging in settings:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📞 Support

If you encounter issues:
1. Check the Django documentation
2. Verify your email provider's SMTP settings
3. Test with a simple email client first
4. Check Django logs for error messages

## 🔄 Next Steps

After configuring email:
1. Test with the management command
2. Set up automated notifications
3. Configure email templates
4. Set up email scheduling
5. Monitor email delivery

---

**Note**: Always test email functionality in development before deploying to production!


