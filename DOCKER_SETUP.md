# Docker Setup Guide

## Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

## Quick Start

### 1. Start the application
```bash
docker-compose up -d
```
This will:
- Build the Django application container
- Start PostgreSQL database
- Run database migrations automatically
- Start the development server on http://localhost:8000

### 2. Load demo data (optional)
```bash
docker-compose exec web python manage.py load_demo_data
```
This creates sample users and tasks:
- Demo user: `demo` / `demo123`
- Admin user: `admin` / `admin123`

### 3. Create superuser (optional)
```bash
docker-compose exec web python manage.py createsuperuser
```

## Common Commands

### View logs
```bash
# All services
docker-compose logs -f

# Only web service
docker-compose logs -f web
```

### Stop the application
```bash
docker-compose down
```

### Stop and remove all data
```bash
docker-compose down -v
```

### Restart services
```bash
docker-compose restart
```

### Run tests
```bash
docker-compose exec web pytest
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Database migrations
```bash
# Create new migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate
```

## Troubleshooting

### Port already in use
If port 8000 or 5432 is already in use, you can change it in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8001 to your preferred port
```

### Permission issues
If you encounter permission issues, ensure the Docker daemon is running and your user has Docker permissions.

### Database connection issues
The web service waits for the database to be ready. If issues persist, check logs:
```bash
docker-compose logs db
```

## Access Points
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/