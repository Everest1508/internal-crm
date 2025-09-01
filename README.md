# CRM Dashboard Django - Business Management Platform

![version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![Django](https://img.shields.io/badge/Django-4.2-green.svg) ![Python](https://img.shields.io/badge/Python-3.12-blue.svg)

A comprehensive **Customer Relationship Management (CRM) system** built with Django and Bootstrap 5. This platform provides a complete solution for managing clients, projects, payments, and business operations with a modern, responsive interface.

> **Built for Business Growth** - Streamline your client relationships, track project progress, and manage payments all in one place.

<br />

## 🚀 Features

### Core CRM Functionality
- **Client Management** - Complete client database with contact information
- **Project Tracking** - Manage projects with requirements, progress, and budgets
- **Payment Management** - Track installments, payments, and financial records
- **Dashboard Analytics** - Real-time insights into your business performance

### Technical Features
- **Modern UI** - Clean, responsive Bootstrap 5 design
- **Multi-user Support** - Team collaboration with user authentication
- **Email Integration** - Custom SMTP configuration for client communications
- **Payment Tracking** - Smart installment management with budget validation
- **Real-time Updates** - Live dashboard with current business metrics

### Developer Features
- **Django 4.2** - Modern Python web framework
- **REST API** - Built-in API endpoints for data access
- **Database Flexibility** - SQLite (default), MySQL, PostgreSQL support
- **WhiteNoise** - Optimized static file serving
- **Docker Ready** - Container deployment support

<br />

## 📊 Dashboard Overview

The CRM Dashboard provides:
- **Total Clients** - Complete client database
- **Active Projects** - Current project status
- **Total Income** - Sum of all paid installments
- **Recent Activity** - Latest projects and payments
- **Monthly Analytics** - Income trends and project metrics

<br />

## 🛠 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
$ git clone <your-repo-url>
$ cd crm-dashboard-django
```

2. **Create virtual environment**
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
$ pip install -r requirements.txt
```

4. **Set up database**
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

5. **Create superuser**
```bash
$ python manage.py createsuperuser
```

6. **Start the application**
```bash
$ python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access your CRM Dashboard.

<br />

## 📁 Project Structure

```
crm-dashboard-django/
├── apps/
│   ├── clients/          # Client management
│   ├── projects/         # Project tracking
│   ├── payments/         # Payment management
│   ├── crm/             # Main CRM functionality
│   └── api/             # REST API endpoints
├── config/              # Django settings
├── templates/           # HTML templates
├── static/             # CSS, JS, images
└── requirements.txt    # Python dependencies
```

<br />

## 🎯 Key Functionality

### Client Management
- Add, edit, and view client information
- Contact details and communication history
- Project association and tracking

### Project Management
- Create projects with budgets and timelines
- Track project requirements and progress
- Assign projects to team members
- Monitor project completion status

### Payment System
- Create payment installments
- Track payment status (pending, paid, overdue)
- Budget validation to prevent overpayment
- Financial reporting and analytics

### Email Integration
- Custom SMTP configuration
- Send emails to clients
- Email logging and tracking
- Template-based communications

<br />

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### SMTP Configuration
Configure email settings in the admin panel or through the web interface:
- SMTP Host
- Port (587 for TLS, 465 for SSL)
- Authentication credentials
- From email address

<br />

## 📈 Business Intelligence

The dashboard provides comprehensive business insights:
- **Income Tracking** - Total and monthly revenue
- **Project Analytics** - Completion rates and timelines
- **Client Metrics** - Client acquisition and retention
- **Payment Status** - Outstanding and overdue payments

<br />

## 🚀 Deployment

### Production Deployment
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure email settings
5. Deploy to your preferred platform

### Docker Deployment
```bash
$ docker build -t crm-dashboard .
$ docker run -p 8000:8000 crm-dashboard
```

<br />

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

<br />

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<br />

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

<br />

---

**CRM Dashboard Django** - Empowering businesses with modern relationship management tools.