# 🗂️ MyPlanner

**MyPlanner** is a personal task-management web application built with **Django** and **PostgreSQL**.  
It allows users to create and organize tasks in custom lists, assign priorities and tags, add reminders, track deadlines, and optionally link tasks with events.  
The project demonstrates both **classic HTML views** (for browser users) and a **REST API** (for integration with future mobile/React apps).

---

## ✨ Features

### 🔑 Authentication
- User registration and login (Django Auth).
- Session-based authentication.
- Some views accessible only to logged-in users.

### ✅ Tasks
- Create, edit, delete tasks.
- Mark tasks as **done/undone** (AJAX toggle).
- Assign tasks to lists and tags.
- Set priority levels and due dates.
- Attach comments for collaboration/notes.

### 📋 To-Do Lists
- Group tasks into **custom lists**.
- View details of each list with its tasks.
- Create, edit, delete lists.

### 🏷️ Tags
- Reuse tags across tasks.
- Colorful tag display for easier navigation.

### ⚙️ Settings
- Manage personal tags in one place.
- Bulk delete tags permanently from the database.
- "Select all" helper button for quick removal.

### ⏰ Reminders
- Add reminders with a timestamp and note.
- Reminders tied directly to tasks.
- Delete reminders when no longer needed.

### 📅 Events
- Optionally link a **calendar-style event** (start/end time) to a task.
- Edit or delete events.
- Prevent duplicate events per task.

### 🔍 Filters
- Filter tasks by:
  - Search text
  - List
  - Priority
  - Done/undone
  - Tags (multi-select)
- Results shown in a clean table.

### 🌐 REST API
- CRUD endpoints for Lists, Tasks, Reminders, Events, and Tags.
- Authentication required.
- Pagination, search, and ordering support.

---

## 🛠️ Tech Stack

- **Backend:** Django 5, Django REST Framework  
- **Database:** PostgreSQL  
- **Frontend:** Classic Django templates (HTML, CSS, JS)  
- **Testing:** Pytest with fixtures for users, tasks, lists  
- **Other:** Custom template filters, CSRF protection, REST API  

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Virtualenv recommended

### 2. Clone the repository
- git clone https://github.com/your-username/myplanner.git
- cd myplanner

### 3) Create and activate a virtual environment
- python -m venv env
### macOS/Linux 
- source env/bin/activate
### Windows
- env\Scripts\activate

### 4) Install dependencies
- pip install -r requirements.txt

### 5) Configure PostgreSQL
Option A: PostgreSQL (recommended for development)
	1.	Create a database named my_planner_db in PostgreSQL.
	2.	Copy .env.example to .env:
```bash
cp .env.example .env
```
	3.	Uncomment and adjust Postgres values in .env:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=my_planner_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

Option B: SQLite (default fallback)
If .env is missing or Postgres values are not set, the project will run on SQLite automatically.
A file db.sqlite3 will be created locally in the project root.

### 6) Apply migrations
```bash
python manage.py migrate
```
### 7) Optional: Create a superuser (only if you want to access Django Admin):
```bash
python manage.py createsuperuser
```
### 8) Run the development server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/ → login/register page.

⸻

### 🧭 Useful URLs (HTML UI)
- Home: /
- Tasks: /app/tasks
- Lists: /app/lists
- Filters: /app/filters
- Settings (Bulk Tag Delete): /app/settings
- Admin: /admin/

⸻

### 🌐 API Endpoints (DRF)
All endpoints are under `/api/` and require authentication.

- **TypeToDoList**
  - List/Create: `/api/type-lists/`
  - Detail (R/U/D): `/api/type-lists/<id>/`

- **Task**
  - List/Create: `/api/tasks/`
  - Detail (R/U/D): `/api/tasks/<id>/`

- **Reminder**
  - List/Create: `/api/reminders/`
  - Detail (R/U/D): `/api/reminders/<id>/`

- **Event**
  - List/Create: `/api/events/`
  - Detail (R/U/D): `/api/events/<id>/`

- **Tag**
  - List/Create: `/api/tags/`
  - Detail (R/U/D): `/api/tags/<id>/`

Auth helper (login/logout UI for DRF): `/api-auth/`

⸻

### 🧪 Running Tests
- pytest
- Pytest will use fixtures from planner/tests/ (users, lists, tasks) and validate task/reminder views behavior.

⸻

### 📂 Project Structure
	•	my_planner_project/
	•	planner/ — main Django app
	•	templates/planner/ — HTML templates (tasks, lists, filters, settings, …)
	•	static/planner/css/ — stylesheets
	•	models.py — models: TypeToDoList, Task, Tag, Reminder, Comment, Event
	•	forms.py — forms: TaskForm, TypeToDoListForm, ReminderForm, EventForm, …
	•	views_html.py — classic HTML views (login required)
	•	views.py — REST API views (DRF generics)
	•	urls_html.py — routes for HTML UI
	•	urls.py — routes for REST API
	•	serializers.py — DRF ModelSerializers
	•	templatetags/ — custom filters (e.g. planner_extras.list_hue)
	•	tests/ — pytest test cases
	•	my_planner_project/ — Django project config (settings, root urls, wsgi)
	•	manage.py
	•	README.md

⸻

### 🔐 Environment & Security Notes
- Keep SECRET_KEY private in production (move to environment variable).
- Set DEBUG = False and configure ALLOWED_HOSTS.
- Use strong DB credentials and non-default PostgreSQL user.

⸻

### 📜 License
- This project is proprietary software.
- © 2025 Jiří Eifler. 
- All rights reserved. 
- No part of this repository may be copied, modified, distributed, or used without explicit written permission from the author.

