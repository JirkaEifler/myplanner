# 🗂️ MyPlanner

> A comprehensive personal task management web application built with Django and PostgreSQL

![License](https://img.shields.io/badge/license-Proprietary-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-14+-blue)

## Overview

MyPlanner is a full-featured task management web application that combines the power of Django's server-side rendering with a modern REST API architecture. The application enables users to organize their work through customizable task lists, priority systems, tagging, and integrated calendar events.

### Key Capabilities

- **Complete Task Management**: Create, organize, and track tasks with advanced filtering and search capabilities
- **Flexible Organization**: Custom lists and reusable color-coded tags for personalized workflow organization
- **Time Management**: Due dates, reminders, and optional calendar event integration
- **Dual Architecture**: Traditional web interface plus REST API for future mobile/frontend integrations
- **Collaboration Features**: Task comments and shared organizational tools

## ✨ Features

### 🔐 Authentication & Security
- Secure user registration and authentication using Django's built-in system
- Session-based authentication with CSRF protection
- Role-based access control for protected resources

### ✅ Task Management
- **Full CRUD Operations**: Create, read, update, and delete tasks with comprehensive form validation
- **Status Management**: Real-time task completion toggling using AJAX
- **Organization Tools**: Assign tasks to custom lists and apply multiple tags
- **Priority System**: Multi-level priority assignment for effective task triage
- **Deadline Tracking**: Due date management with visual indicators
- **Collaborative Notes**: Attach comments for team collaboration or personal notes

### 📂 List Organization
- **Custom Lists**: Create unlimited personalized task lists for different projects or contexts
- **List Management**: Edit list properties, view task summaries, and manage list-specific workflows
- **Hierarchical Organization**: Organize tasks within lists for better project management

### 🏷️ Tag System
- **Flexible Tagging**: Create and reuse tags across all tasks
- **Visual Organization**: Color-coded tag system for quick visual identification
- **Tag Management**: Centralized tag administration with bulk operations

### ⚙️ Advanced Settings
- **Tag Administration**: Comprehensive tag management interface
- **Bulk Operations**: Select and delete multiple tags efficiently
- **Data Management**: Clean database maintenance tools

### ⏰ Reminder System
- **Custom Reminders**: Set timestamped reminders with personalized notes
- **Task Integration**: Direct linking between reminders and specific tasks
- **Reminder Management**: Create, edit, and delete reminders as needed

### 📅 Event Integration
- **Calendar Events**: Link tasks with calendar-style events including start and end times
- **Event Management**: Full CRUD operations for event scheduling
- **Duplicate Prevention**: System prevents multiple events per task for data integrity

### 🔍 Advanced Filtering
- **Multi-Criteria Search**: Filter tasks by text content, list assignment, priority level, and completion status
- **Tag-Based Filtering**: Multi-select tag filtering for precise task discovery
- **Results Display**: Clean, tabular presentation of filtered results

### 🌐 REST API
- **Complete API Coverage**: Full CRUD endpoints for all major entities (Lists, Tasks, Reminders, Events, Tags)
- **Authentication Required**: Secure API access with user-based permissions
- **Advanced Features**: Built-in pagination, search capabilities, and flexible result ordering
- **Integration Ready**: Designed for future mobile applications or React frontend integration

## 🛠️ Technical Architecture

### Backend Stack
- **Framework**: Django 5.x with Django REST Framework
- **Database**: PostgreSQL 14+ (with SQLite fallback for development)
- **Authentication**: Django's built-in authentication system
- **API**: RESTful API architecture with comprehensive serialization

### Frontend Implementation
- **Templates**: Django template system with custom template tags and filters
- **Styling**: Custom CSS with responsive design principles
- **Interactivity**: JavaScript for AJAX functionality and dynamic user interactions
- **User Experience**: Progressive enhancement with graceful degradation

### Quality Assurance
- **Testing Framework**: Pytest with comprehensive test coverage
- **Test Fixtures**: Pre-configured test data for users, tasks, and lists
- **Validation**: Form validation and API endpoint testing

## Installation & Setup

### Prerequisites

Ensure your development environment includes:

- **Python**: Version 3.11 or higher
- **PostgreSQL**: Version 14 or higher (recommended)
- **Virtual Environment**: Python venv or virtualenv

### 🚀 Getting Started

1. **Repository Setup**
   ```bash
   git clone https://github.com/your-username/myplanner.git
   cd myplanner
   ```

2. **Environment Configuration**
   ```bash
   # Create virtual environment
   python -m venv env
   
   # Activate virtual environment
   # On macOS/Linux:
   source env/bin/activate
   # On Windows:
   env\Scripts\activate
   ```

3. **Dependency Installation**
   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

#### Option A: PostgreSQL (Recommended)

1. **Create Database**
   ```sql
   -- In PostgreSQL console
   CREATE DATABASE my_planner_db;
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   ```

3. **Configure Database Settings**
   
   Edit `.env` file with your PostgreSQL credentials:
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=my_planner_db
   DB_USER=postgres
   DB_PASSWORD=your_secure_password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

#### Option B: SQLite (Quick Start / Default)

If no `.env` file is configured, the application automatically falls back to SQLite with a local `db.sqlite3` file in the project root.

### Application Initialization

1. **Database Migration**
   ```bash
   python manage.py migrate
   ```

2. **Administrative User Creation** (Optional)
   ```bash
   python manage.py createsuperuser
   ```

3. **Development Server**
   ```bash
   python manage.py runserver
   ```

   Access the application at: `http://127.0.0.1:8000/`

## Application Structure

### 🧭 Web Interface Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page and authentication |
| `/app/tasks/` | Main task management interface |
| `/app/lists/` | List creation and management |
| `/app/filters/` | Advanced task filtering tools |
| `/app/settings/` | Tag management and bulk operations |
| `/admin/` | Django administrative interface |

### 🌐 REST API Endpoints

All API endpoints require authentication and are prefixed with `/api/`.

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/type-lists/` | GET, POST | List and create task lists |
| `/api/type-lists/<id>/` | GET, PUT, PATCH, DELETE | Individual list operations |
| `/api/tasks/` | GET, POST | List and create tasks |
| `/api/tasks/<id>/` | GET, PUT, PATCH, DELETE | Individual task operations |
| `/api/reminders/` | GET, POST | List and create reminders |
| `/api/reminders/<id>/` | GET, PUT, PATCH, DELETE | Individual reminder operations |
| `/api/events/` | GET, POST | List and create events |
| `/api/events/<id>/` | GET, PUT, PATCH, DELETE | Individual event operations |
| `/api/tags/` | GET, POST | List and create tags |
| `/api/tags/<id>/` | GET, PUT, PATCH, DELETE | Individual tag operations |
| `/api-auth/` | GET, POST | DRF authentication interface |

### API Features

- **Pagination**: Configurable page size for large datasets
- **Search**: Full-text search across relevant fields
- **Ordering**: Flexible result sorting by multiple criteria
- **Filtering**: Query parameter-based filtering options

## Development

### 📂 Project Structure

```
myplanner/
├── my_planner_project/          # Django project configuration
│   ├── settings.py             # Application settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI application entry point
├── planner/                    # Main application module
│   ├── models.py              # Data models (Task, List, Tag, etc.)
│   ├── views_html.py          # Traditional HTML views
│   ├── views.py               # REST API views
│   ├── forms.py               # Django forms for HTML interface
│   ├── serializers.py         # DRF serializers for API
│   ├── urls_html.py           # HTML interface URL patterns
│   ├── urls.py                # API URL patterns
│   ├── templatetags/          # Custom template filters
│   ├── templates/planner/     # HTML templates
│   ├── static/planner/        # CSS and JavaScript assets
│   └── tests/                 # Test suite
├── requirements.txt           # Python dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

### 🧪 Running Tests

Execute the complete test suite:

```bash
pytest
```

The test suite includes:
- **Model Testing**: Validation of data models and relationships
- **View Testing**: HTTP response validation for both HTML and API endpoints
- **Form Testing**: Input validation and error handling
- **Integration Testing**: End-to-end workflow validation

### Code Quality

The project follows Django best practices including:

- **Security**: CSRF protection, SQL injection prevention, XSS mitigation
- **Performance**: Optimized database queries and efficient template rendering
- **Maintainability**: Clear separation of concerns between HTML views and API endpoints
- **Scalability**: Database-agnostic design with PostgreSQL optimization

## Deployment Considerations

### 🔐 Security Configuration

Before deploying to production:

1. **Secret Key Management**
   - Move `SECRET_KEY` to environment variables
   - Use cryptographically secure key generation

2. **Debug Configuration**
   - Set `DEBUG = False` in production settings
   - Configure appropriate `ALLOWED_HOSTS`

3. **Database Security**
   - Use strong, unique database credentials
   - Avoid default PostgreSQL users in production
   - Implement proper network security for database access

### ⚡️ Performance Optimization

- Configure static file serving for production
- Implement database connection pooling
- Consider caching strategies for frequently accessed data
- Optimize database queries with select_related/prefetch_related

## 📧 Contributing

This is proprietary software. Please contact the author for contribution guidelines and licensing information.
email: jirka.eifler@gmail.com

## 📜 License

© 2025 Jiří Eifler. All rights reserved.

This project is proprietary software. No part of this repository may be copied, modified, distributed, or used without explicit written permission from the author.
