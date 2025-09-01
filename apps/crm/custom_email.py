import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from .models import CustomSMTPConfig, EmailLog

logger = logging.getLogger(__name__)


class CustomEmailSender:
    """Custom email sender using Python smtplib"""
    
    def __init__(self, smtp_config_id=None):
        """
        Initialize with SMTP configuration
        
        Args:
            smtp_config_id: ID of CustomSMTPConfig to use, or None for active config
        """
        if smtp_config_id:
            self.smtp_config = CustomSMTPConfig.objects.get(id=smtp_config_id)
        else:
            # Get the first active configuration
            self.smtp_config = CustomSMTPConfig.objects.filter(is_active=True).first()
        
        if not self.smtp_config:
            raise ValueError("No active SMTP configuration found")
    
    def send_email(self, recipient, subject, message, html_message=None, attachments=None, user=None):
        """
        Send email using custom SMTP configuration
        
        Args:
            recipient: Email address or list of email addresses
            subject: Email subject
            message: Plain text message
            html_message: HTML message (optional)
            attachments: List of file paths to attach (optional)
            user: User sending the email (for logging)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_config.from_email
            msg['To'] = recipient if isinstance(recipient, str) else ', '.join(recipient)
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(message, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_message:
                html_part = MIMEText(html_message, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {file_path.split("/")[-1]}'
                        )
                        msg.attach(part)
                    except Exception as e:
                        logger.warning(f"Failed to attach file {file_path}: {e}")
            
            # Create SMTP connection
            if self.smtp_config.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_config.smtp_host, self.smtp_config.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_config.smtp_host, self.smtp_config.smtp_port)
            
            # Start TLS if required
            if self.smtp_config.use_tls and not self.smtp_config.use_ssl:
                server.starttls(context=ssl.create_default_context())
            
            # Login
            server.login(self.smtp_config.username, self.smtp_config.password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            # Log successful email
            self._log_email(recipient, subject, message, 'sent', None, user)
            
            logger.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to send email to {recipient}: {error_msg}")
            
            # Log failed email
            self._log_email(recipient, subject, message, 'failed', error_msg, user)
            
            return False
    
    def _log_email(self, recipient, subject, message, status, error_message, user):
        """Log email attempt to database"""
        try:
            EmailLog.objects.create(
                smtp_config=self.smtp_config,
                recipient=recipient if isinstance(recipient, str) else ', '.join(recipient),
                subject=subject,
                message=message,
                status=status,
                error_message=error_message,
                sent_by=user
            )
        except Exception as e:
            logger.error(f"Failed to log email: {e}")
    
    def test_connection(self):
        """Test SMTP connection without sending email"""
        try:
            if self.smtp_config.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_config.smtp_host, self.smtp_config.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_config.smtp_host, self.smtp_config.smtp_port)
            
            if self.smtp_config.use_tls and not self.smtp_config.use_ssl:
                server.starttls(context=ssl.create_default_context())
            
            server.login(self.smtp_config.username, self.smtp_config.password)
            server.quit()
            
            return True, "Connection successful"
            
        except Exception as e:
            return False, str(e)


def send_custom_email(recipient, subject, message, html_message=None, attachments=None, smtp_config_id=None, user=None):
    """
    Convenience function to send email using custom SMTP
    
    Args:
        recipient: Email address or list of email addresses
        subject: Email subject
        message: Plain text message
        html_message: HTML message (optional)
        attachments: List of file paths to attach (optional)
        smtp_config_id: ID of CustomSMTPConfig to use (optional)
        user: User sending the email (for logging)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        sender = CustomEmailSender(smtp_config_id)
        return sender.send_email(recipient, subject, message, html_message, attachments, user)
    except Exception as e:
        logger.error(f"Failed to create email sender: {e}")
        return False


def test_smtp_connection(smtp_config_id=None):
    """
    Test SMTP connection
    
    Args:
        smtp_config_id: ID of CustomSMTPConfig to test (optional)
    
    Returns:
        tuple: (success, message)
    """
    try:
        sender = CustomEmailSender(smtp_config_id)
        return sender.test_connection()
    except Exception as e:
        return False, str(e)


def get_available_smtp_configs():
    """Get list of available SMTP configurations"""
    return CustomSMTPConfig.objects.filter(is_active=True).order_by('name')


def get_email_logs(limit=50):
    """Get recent email logs"""
    return EmailLog.objects.all().order_by('-sent_at')[:limit]


