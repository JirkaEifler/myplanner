# MyPlanner

A comprehensive personal task management web application built with Django and PostgreSQL. MyPlanner enables users to create, organize, and track tasks through custom lists, priorities, tags, reminders, and calendar events. The application features both a traditional web interface and a REST API for future mobile and third-party integrations.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔑 User Authentication
- **Secure Registration & Login** - Django's built-in authentication system
- **Session Management** - Persistent user sessions across devices
- **Protected Routes** - Role-based access to sensitive functionality

### ✅ Task Management
- **CRUD Operations** - Create, read, update, and delete tasks
- **Status Tracking** - Real-time AJAX toggle for task completion
- **Organization** - Assign tasks to custom lists and tags
- **Priority System** - Multiple priority levels for task importance
- **Deadline Management** - Due date tracking with visual indicators
- **Collaborative Notes** - Add comments for team coordination

### 📋 List Organization
- **Custom Lists** - Group related tasks into personalized categories  
- **List Management** - Full CRUD operations for list organization
- **Task Overview** - Comprehensive view of tasks within each list
- **Flexible Structure** - Unlimited lists per user

### 🏷️ Tag System
- **Reusable Tags** - Apply tags across multiple tasks
- **Visual Design** - Color-coded tags for quick identification
- **Bulk Management** - Efficient tag creation and deletion
- **Cross-filtering** - Use tags for advanced task filtering

### ⚙️ Settings & Preferences
- **Tag Management Hub** - Centralized tag administration
- **Bulk Operations** - Mass delete functionality with safety checks
- **Quick Actions** - "Select all" helpers for efficient management

### ⏰ Smart Reminders
- **Flexible Scheduling** - Set custom reminder timestamps
- **Contextual Notes** - Add specific reminder messages
- **Task Integration** - Direct linking between reminders and tasks
- **Easy Cleanup** - Simple reminder deletion when completed

### 📅 Event Integration
- **Calendar Sync** - Link tasks with calendar-style events
- **Time Blocking** - Set start and end times for task completion
- **Event Management** - Edit or remove events independently
- **Duplicate Prevention** - Automatic validation against multiple events per task

### 🔍 Advanced Filtering
- **Multi-criteria Search** - Filter by text, list, priority, status
- **Tag-based Filtering** - Multi-select tag combinations
- **Real-time Results** - Instant filtering with clean table display
- **Saved Views** - Remember filter preferences

### 🌐 REST API
- **Complete CRUD** - Full API coverage for all data models
- **Authentication Required** - Secure endpoints with user validation
- **Modern Features** - Pagination, search, and ordering support
- **Developer Friendly** - Consistent JSON responses and error handling

## 🛠️ Tech Stack

| Category | Technology | Version |
|----------|------------|---------|
| **Backend Framework** | Django | 5.x |
| **API Framework** | Django REST Framework | Latest |
| **Database** | PostgreSQL | 14+ |
| **Frontend** | Django Templates | HTML5/CSS3/JS |
| **Testing** | Pytest | Latest |
| **Authentication** | Django Auth | Built-in |

## 📋 Prerequisites

- **Python** 3.11 or higher
- **PostgreSQL** 14 or higher  
- **Virtual Environment** (recommended)
- **Git** for version control

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/myplanner.git
cd myplanner
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# macOS/Linux
source env/bin/activate

# Windows
env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=my_planner_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

## ⚙️ Configuration

### Database Setup

1. **Create PostgreSQL Database**
   ```sql
   CREATE DATABASE my_planner_db;
   CREATE USER planner_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE my_planner_db TO planner_user;
   ```

2. **Update Django Settings**
   ```python
   # my_planner_project/settings.py
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "HOST": os.getenv("DB_HOST", "127.0.0.1"),
           "PORT": os.getenv("DB_PORT", "5432"),
           "NAME": os.getenv("DB_NAME", "my_planner_db"),
           "USER": os.getenv("DB_USER", "postgres"),
           "PASSWORD": os.getenv("DB_PASSWORD"),
       }
   }
   ```

### 3. Initialize Database
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Access the application at **http://127.0.0.1:8000/**

## 🎯 Usage

### Web Interface Navigation

| Feature | URL | Description |
|---------|-----|-------------|
| **Home** | `/` | Dashboard overview |
| **Tasks** | `/app/tasks/` | Task management interface |
| **Lists** | `/app/lists/` | List organization |
| **Filters** | `/app/filters/` | Advanced task filtering |
| **Settings** | `/app/settings/` | Tag management and preferences |
| **Admin** | `/admin/` | Django admin interface |

### Quick Start Guide

1. **Create Your First List**
   - Navigate to `/app/lists/`
   - Click "Create New List"
   - Name your list and add description

2. **Add Tasks**
   - Go to `/app/tasks/`
   - Click "Add Task"
   - Fill in details: name, description, priority, due date
   - Assign to a list and add tags

3. **Set Reminders**
   - Edit any task
   - Add reminder timestamp and note
   - Save to activate reminder

4. **Filter and Search**
   - Use `/app/filters/` for advanced searching
   - Combine multiple criteria for precise results

## 🌐 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication
All API endpoints require authentication. Include session cookies or use DRF's token authentication.

### Endpoints Overview

#### Lists Management
```http
GET    /api/type-lists/          # List all lists
POST   /api/type-lists/          # Create new list
GET    /api/type-lists/{id}/     # Get specific list
PUT    /api/type-lists/{id}/     # Update list
DELETE /api/type-lists/{id}/     # Delete list
```

#### Task Operations
```http
GET    /api/tasks/               # List all tasks
POST   /api/tasks/               # Create new task
GET    /api/tasks/{id}/          # Get specific task
PUT    /api/tasks/{id}/          # Update task
DELETE /api/tasks/{id}/          # Delete task
```

#### Reminders
```http
GET    /api/reminders/           # List all reminders
POST   /api/reminders/           # Create new reminder
GET    /api/reminders/{id}/      # Get specific reminder
PUT    /api/reminders/{id}/      # Update reminder
DELETE /api/reminders/{id}/      # Delete reminder
```

#### Events
```http
GET    /api/events/              # List all events
POST   /api/events/              # Create new event
GET    /api/events/{id}/         # Get specific event
PUT    /api/events/{id}/         # Update event
DELETE /api/events/{id}/         # Delete event
```

#### Tags
```http
GET    /api/tags/                # List all tags
POST   /api/tags/                # Create new tag
GET    /api/tags/{id}/           # Get specific tag
PUT    /api/tags/{id}/           # Update tag
DELETE /api/tags/{id}/           # Delete tag
```

### API Features
- **Pagination** - Configurable page sizes
- **Filtering** - URL parameter-based filtering
- **Searching** - Text search across relevant fields
- **Ordering** - Sort by any field (ascending/descending)

### Sample API Request
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/" \
     -H "Authorization: Token your-token-here" \
     -H "Content-Type: application/json"
```

### Sample API Response
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/tasks/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Complete project documentation",
            "description": "Write comprehensive README",
            "priority": "high",
            "due_date": "2025-09-01",
            "is_done": false,
            "list": 2,
            "tags": [1, 3, 5],
            "created_at": "2025-08-30T10:00:00Z"
        }
    ]
}
```

## 📂 Project Structure

```
myplanner/
├── my_planner_project/          # Django project configuration
│   ├── settings.py             # Main settings file
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── planner/                     # Main Django application
│   ├── models.py               # Database models
│   ├── views.py                # REST API views
│   ├── views_html.py           # HTML template views
│   ├── forms.py                # Django forms
│   ├── serializers.py          # DRF serializers
│   ├── urls.py                 # API URL patterns
│   ├── urls_html.py            # HTML URL patterns
│   ├── admin.py                # Django admin configuration
│   ├── templatetags/           # Custom template filters
│   │   └── planner_extras.py   # Custom template tags
│   ├── templates/planner/      # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── tasks/              # Task-related templates
│   │   ├── lists/              # List management templates
│   │   └── filters/            # Filtering interface
│   ├── static/planner/         # Static files
│   │   ├── css/                # Stylesheets
│   │   ├── js/                 # JavaScript files
│   │   └── images/             # Image assets
│   └── tests/                  # Test suite
│       ├── conftest.py         # Pytest configuration
│       ├── test_models.py      # Model tests
│       ├── test_views.py       # View tests
│       └── fixtures/           # Test data fixtures
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=planner

# Run specific test file
pytest planner/tests/test_models.py

# Run with verbose output
pytest -v
```

### Test Coverage
The test suite includes:
- **Model Tests** - Database model validation
- **View Tests** - HTTP endpoint functionality  
- **Form Tests** - Input validation and processing
- **API Tests** - REST endpoint behavior
- **Integration Tests** - End-to-end workflows

### Test Fixtures
Pre-built fixtures available:
- `user_fixture` - Test users with different roles
- `list_fixture` - Sample to-do lists
- `task_fixture` - Various task configurations
- `tag_fixture` - Common tags for testing

## 🔐 Security

### Production Checklist

- [ ] **Environment Variables** - Move all secrets to environment variables
- [ ] **Debug Mode** - Set `DEBUG = False` in production
- [ ] **Allowed Hosts** - Configure `ALLOWED_HOSTS` properly
- [ ] **Database Security** - Use strong credentials and restricted access
- [ ] **HTTPS** - Enable SSL/TLS encryption
- [ ] **CSRF Protection** - Verify CSRF tokens are working
- [ ] **SQL Injection** - Use Django ORM (already protected)
- [ ] **XSS Protection** - Template auto-escaping enabled

### Security Features
- **Authentication Required** - Protected routes for sensitive operations
- **CSRF Protection** - All forms include CSRF tokens
- **SQL Injection Prevention** - Django ORM provides automatic protection
- **XSS Prevention** - Template auto-escaping enabled by default
- **Session Security** - Secure session configuration

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
   ```bash
   git fork https://github.com/your-username/myplanner.git
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **Make changes and test**
   ```bash
   # Make your changes
   pytest  # Run tests
   ```

4. **Commit with clear message**
   ```bash
   git commit -m "Add: Amazing new feature for task automation"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/amazing-new-feature
   ```

### Contribution Guidelines

- **Code Style** - Follow PEP 8 for Python code
- **Documentation** - Update docstrings and comments
- **Testing** - Add tests for new functionality
- **Security** - Follow Django security best practices
- **Commits** - Use conventional commit messages

### Code Style
```python
# Good example
def create_task(user: User, title: str, priority: str = 'medium') -> Task:
    """
    Create a new task for the specified user.
    
    Args:
        user (User): The user who owns the task
        title (str): Task title
        priority (str): Task priority level
        
    Returns:
        Task: The created task instance
    """
    return Task.objects.create(
        user=user,
        title=title,
        priority=priority
    )
```

## 🆘 Support

### Common Issues

**Q: Database connection errors**
```bash
# Check PostgreSQL service status
sudo service postgresql status

# Verify database exists
psql -U postgres -l
```

**Q: Migration conflicts**
```bash
# Reset migrations (development only)
python manage.py migrate planner zero
python manage.py makemigrations planner
python manage.py migrate
```

**Q: Static files not loading**
```bash
# Collect static files
python manage.py collectstatic
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/your-username/myplanner/issues)
- **Documentation**: [Project Wiki](https://github.com/your-username/myplanner/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/myplanner/discussions)

### Performance Tips

- **Database Indexing** - Add indexes for frequently queried fields
- **Query Optimization** - Use `select_related()` and `prefetch_related()`
- **Caching** - Implement Redis for session and page caching
- **Media Files** - Use CDN for static file delivery in production

## 📄 License

**Proprietary Software**

© 2025 Jiří Eifler. All rights reserved.

This software is proprietary and confidential. No part of this repository may be copied, modified, distributed, or used without explicit written permission from the author.

For licensing inquiries, please contact: jirka.eifler@gmail.com

---

**Built with ❤️ using Django and PostgreSQL**