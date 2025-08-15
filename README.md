# Entirius Template Django Service

A template Django service for the Entirius e-commerce AI platform, following the modular monolith architecture pattern. This template demonstrates best practices for creating new Django-based services within the Entirius ecosystem.

## Features

- **Django 5.2+** with Django REST Framework
- **Pydantic** integration for API validation (ADR-002)
- **OpenAPI 3.0** schema generation with drf-spectacular
- **UV** package management for fast dependency installation (ADR-007)
- **Ruff** linting and formatting (ADR-010)
- **Comprehensive test coverage** with pytest
- **Example CRUD operations** with proper error handling
- **Authentication and permissions** setup
- **Production-ready** configuration patterns

## Architecture

This service follows [ADR-001 Modular Monolith](../../docs-entirius/docs/adr/adr-001-modular-monolith.md) architecture and [ADR-002 Django REST Framework with Pydantic](../../docs-entirius/docs/adr/adr-002-openapi-django-rest-framework.md) for API development.

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager (install from [astral-sh.github.io/uv](https://astral-sh.github.io/uv/))

### Installation

1. **Create virtual environment and install dependencies:**
```bash
# Navigate to service directory
cd services/entirius-service-template-django/

# Create virtual environment and sync dependencies
uv venv
uv sync --dev

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows
```

2. **Set up database:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

3. **Run development server:**
```bash
python manage.py runserver
```

4. **Access the service:**
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/schema/swagger-ui/
- ReDoc Documentation: http://localhost:8000/api/schema/redoc/

## Development

### Code Quality Commands

```bash
# Lint and format code
ruff check .
ruff format .

# Type checking
mypy .

# Run tests
pytest

# Run tests with coverage
pytest --cov=apps --cov-report=html --cov-report=term
```

### API Documentation

The service automatically generates OpenAPI 3.0 documentation using drf-spectacular:

- **Swagger UI**: `/api/schema/swagger-ui/`
- **ReDoc**: `/api/schema/redoc/`
- **OpenAPI Schema**: `/api/schema/`

### Example API Usage

The template includes a complete CRUD example for `ExampleModel`:

```bash
# List items
curl -X GET http://localhost:8000/api/v1/examples/

# Create item
curl -X POST http://localhost:8000/api/v1/examples/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item", "is_active": true}'

# Get specific item
curl -X GET http://localhost:8000/api/v1/examples/1/

# Update item
curl -X PUT http://localhost:8000/api/v1/examples/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'

# Delete item
curl -X DELETE http://localhost:8000/api/v1/examples/1/
```

## Project Structure

```
entirius-service-template-django/
├── apps/                           # Django applications
│   ├── example/                    # Example app demonstrating patterns
│   │   ├── models.py               # Database models
│   │   ├── serializers.py          # Pydantic/DRF serializers
│   │   ├── views.py                # API views
│   │   ├── urls.py                 # URL routing
│   │   ├── admin.py                # Django admin configuration
│   │   └── tests/                  # Test files
│   │       ├── test_models.py
│   │       └── test_views.py
├── main/                           # Django settings
│   ├── settings.py                 # Base settings
│   ├── settings_local.py           # Local/environment settings
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI configuration
│   └── asgi.py                     # ASGI configuration
├── pyproject.toml                  # Project configuration (ADR-013)
├── manage.py                       # Django management script
├── README.md                       # This file
└── CLAUDE.md                       # Claude Code instructions
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://user:password@localhost:5432/db_name

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Celery (optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Database Configuration

For production, configure PostgreSQL in `settings_local.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Creating Your Own Service

1. **Copy this template:**
```bash
cp -r services/entirius-service-template-django/ services/your-new-service-name/
```

2. **Update configuration:**
   - Rename in `pyproject.toml`
   - Update `README.md`
   - Modify `CLAUDE.md`
   - Update API titles in `settings.py`

3. **Replace example app:**
   - Remove or rename `apps/example/`
   - Create your business logic apps
   - Update `settings.py` INSTALLED_APPS
   - Update main `urls.py`

4. **Customize for your domain:**
   - Define your models
   - Create Pydantic serializers
   - Implement business logic in views
   - Write comprehensive tests

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/example/tests/

# Run tests matching pattern
pytest -k "test_example"

# Run tests in parallel
pytest -n auto
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching
- [ ] Set up proper `ALLOWED_HOSTS`
- [ ] Configure static files serving
- [ ] Set up logging
- [ ] Configure SSL/HTTPS
- [ ] Set up monitoring and health checks

### Docker Support

This template is ready for Docker containerization following Entirius deployment patterns.

## Security

The template includes security best practices:

- **Authentication**: Session-based authentication by default
- **Permissions**: Authentication required for all endpoints
- **Validation**: Pydantic models for request validation
- **CSRF Protection**: Enabled for web interfaces
- **SQL Injection**: Protected by Django ORM
- **XSS Protection**: Django's built-in protections

## Contributing

When making changes to this template:

1. Follow the established patterns
2. Update tests for any changes
3. Run the full test suite
4. Update documentation
5. Follow [ADR guidelines](../../docs-entirius/docs/adr/)

## Related Documentation

- [Main Project Documentation](../../docs-entirius/)
- [Architecture Decision Records](../../docs-entirius/docs/adr/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details.