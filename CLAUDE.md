# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the Entirius Template Django Service.

## Service Overview

The Entirius Template Django Service is a template for creating new Django-based backend services within the Entirius e-commerce platform. This service demonstrates best practices, architectural patterns, and development workflows for the modular monolith architecture.

**Architecture**: Part of the modular monolith architecture (ADR-001)  
**Framework**: Django 5.0+ with Django REST Framework (ADR-002)  
**API Standard**: OpenAPI 3.0 with Pydantic validation  
**Package Management**: UV (ADR-007) for 10-100x faster dependency installation
**Build Backend**: Hatchling (ADR-013) for modern Python packaging

## Technology Stack

### Backend Framework
- **Django 5.2+**: Web framework and ORM
- **Django REST Framework**: RESTful API development
- **Pydantic**: Type validation and serialization
- **drf-spectacular**: OpenAPI schema generation

### Database & Storage
- **PostgreSQL**: Primary database (shared with other services in production)
- **SQLite**: Default for development and testing
- **Redis**: Optional caching and session storage
- **Celery**: Optional asynchronous task processing

### Development Tools
- **UV**: Python package manager (replaces pip/venv)
- **Ruff**: Linting and formatting (ADR-010)
- **pytest**: Testing framework
- **mypy**: Static type checking

## Development Commands

### Environment Setup
```bash
# Create virtual environment and sync all dependencies (recommended)
uv venv
uv sync --dev  # Install all dependencies including dev from pyproject.toml

# Alternative: Manual installation (not recommended)
uv pip install -e .         # Install package in editable mode
uv pip install -e ".[dev]"  # Install with dev dependencies

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows
```

### Django Management
```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Code Quality
```bash
# Lint and format code (using Ruff per ADR-010)
ruff check .
ruff format .

# Type checking
mypy .

# Run tests
pytest
pytest --cov=apps --cov-report=html  # with coverage

# Test specific app or module
pytest apps/example/tests/
```

### API Documentation
```bash
# Generate OpenAPI schema
python manage.py spectacular --color --file schema.yml

# View API documentation (development server running)
# Visit: http://localhost:8000/api/schema/swagger-ui/
# Visit: http://localhost:8000/api/schema/redoc/
```

## Project Structure

```
entirius-service-template-django/
├── apps/                           # Django applications
│   ├── example/                    # Example app showing patterns
│   │   ├── models.py               # Database models
│   │   ├── serializers.py          # Pydantic/DRF serializers
│   │   ├── views.py                # API views
│   │   ├── urls.py                 # URL routing
│   │   ├── admin.py                # Django admin
│   │   └── tests/                  # Test files
│   │       ├── test_models.py
│   │       └── test_views.py
├── main/                           # Django settings
│   ├── settings.py                 # Base settings
│   ├── settings_local.py           # Local settings
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI configuration
│   └── asgi.py                     # ASGI configuration
├── pyproject.toml                  # Project configuration (ADR-013)
├── manage.py                       # Django management script
├── README.md                       # Documentation
└── CLAUDE.md                       # This file
```

## API Development Guidelines

### Pydantic Integration (per ADR-002)
```python
# Example Pydantic model for request validation
from pydantic import BaseModel, Field
from typing import List, Optional

class ExampleCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the item")
    description: Optional[str] = Field(None, description="Optional description")
    is_active: bool = Field(True, description="Whether the item is active")

class ExampleResponse(BaseModel):
    id: int = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the item")
    description: str = Field(..., description="Description")
    is_active: bool = Field(..., description="Active status")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    @classmethod
    def from_model(cls, instance: ExampleModel) -> "ExampleResponse":
        """Convert Django model instance to Pydantic response."""
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description or "",
            is_active=instance.is_active,
            created_at=instance.created_at.isoformat(),
            updated_at=instance.updated_at.isoformat(),
        )
```

### ViewSet Pattern
```python
# Example API ViewSet with Pydantic validation
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from pydantic import ValidationError

class ExampleViewSet(ViewSet):
    @extend_schema(
        summary="Create example item",
        request=ExampleCreateRequest,
        responses={201: ExampleResponse}
    )
    def create(self, request):
        try:
            validated_data = ExampleCreateRequest(**request.data)
        except ValidationError as e:
            return Response(
                {"validation_errors": e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Business logic here
        instance = ExampleModel.objects.create(
            name=validated_data.name,
            description=validated_data.description or "",
            is_active=validated_data.is_active,
        )
        
        response_data = ExampleResponse.from_model(instance)
        return Response(response_data.model_dump(), status=status.HTTP_201_CREATED)
```

## Environment Variables

### Required Configuration
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=main.settings

# Database Configuration (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/entirius_template_db

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379/0

# Celery Configuration (Optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Development Configuration
```bash
# Development-specific settings
DEBUG=True
DJANGO_SETTINGS_MODULE=main.settings_local

# Development database (SQLite default)
# No additional configuration needed for SQLite
```

## Testing Strategy

### Test Structure
```bash
apps/
└── example/
    └── tests/
        ├── __init__.py
        ├── test_models.py          # Model tests
        └── test_views.py           # API endpoint tests
```

### Test Commands
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=apps --cov-report=html --cov-report=term

# Run specific test file
pytest apps/example/tests/test_views.py

# Run tests matching pattern
pytest -k "test_example"

# Run tests in parallel (install pytest-xdist)
pytest -n auto
```

## Creating New Services from Template

### Steps to Create a New Service

1. **Copy the template:**
```bash
cp -r services/entirius-service-template-django/ services/your-new-service-name/
cd services/your-new-service-name/
```

2. **Update project configuration:**
   - Edit `pyproject.toml`: Change name, description
   - Edit `README.md`: Update service name and description
   - Edit `CLAUDE.md`: Update service-specific information
   - Edit `main/settings.py`: Update SPECTACULAR_SETTINGS title

3. **Replace example app with your business logic:**
   - Remove or rename `apps/example/`
   - Create new apps: `python manage.py startapp your_app_name apps/`
   - Update `main/settings.py` INSTALLED_APPS
   - Update `main/urls.py` to include your app URLs

4. **Implement your domain logic:**
   - Define models in `models.py`
   - Create Pydantic serializers in `serializers.py`
   - Implement API views in `views.py`
   - Configure URLs in `urls.py`
   - Write comprehensive tests

## Important Notes for Claude Code

### Always Follow ADR Guidelines
- Use **UV** for all Python package management (`uv sync --dev` recommended)
- Use **Hatchling** build backend (configured in pyproject.toml per ADR-013)
- Use **Ruff** for linting and formatting (`ruff check .`, `ruff format .`)
- Follow **Django REST Framework** patterns with **Pydantic** validation
- Maintain **OpenAPI 3.0** schema accuracy with drf-spectacular
- Respect **modular monolith architecture** boundaries
- No `requirements.txt` files - all dependencies in pyproject.toml (ADR-007)

### Development Workflow
1. **Always run tests** after making code changes: `pytest`
2. **Always run linting** before committing: `ruff check . && ruff format .`
3. **Type check** your code: `mypy .`
4. **Validate migrations**: `python manage.py makemigrations --check`
5. **Test API documentation**: Visit `/api/schema/swagger-ui/` during development

### Template Customization Guidelines
- Keep the established patterns and structure
- Follow the Pydantic integration approach for all new APIs
- Maintain comprehensive test coverage
- Update documentation when making changes
- Follow Django and DRF best practices
- Use the same code quality tools configuration

### Database Considerations
- This template uses SQLite for development simplicity
- For production, configure PostgreSQL (shared database per modular monolith)
- Use Django migrations for all schema changes
- Implement proper indexing for performance-critical queries

## Related Documentation

- **Main Project Documentation**: `../../docs-entirius/`
- **Architecture Decision Records**: `../../docs-entirius/docs/adr/`
- **Original AI Gateway Service**: `../entirius-service-ai-gateway/CLAUDE.md`
- **API Documentation**: Available at `/api/schema/swagger-ui/` (development server)

## Template Usage Examples

This template demonstrates:
- ✅ Complete CRUD operations with Pydantic validation
- ✅ OpenAPI 3.0 schema generation
- ✅ Comprehensive test coverage
- ✅ Django admin integration
- ✅ Error handling and validation
- ✅ Production-ready configuration patterns
- ✅ UV package management setup
- ✅ Ruff linting configuration
- ✅ Type hints and mypy integration

Use this template as a starting point for any new Django service in the Entirius platform.