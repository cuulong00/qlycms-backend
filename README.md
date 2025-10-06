# Chatbot Manager Backend

Production-ready FastAPI backend with Clean Architecture, SQLAlchemy 2.0, and comprehensive security.

## 🎯 Features

- ✅ **Clean Architecture** - Separation of concerns with clear layer boundaries
- ✅ **Async/Await** - Full async support for high performance
- ✅ **Type Safety** - Complete type hints with MyPy validation
- ✅ **Security** - JWT auth, OAuth2, RBAC/ABAC with Casbin
- ✅ **Database** - SQLAlchemy 2.0 with async support
- ✅ **Migrations** - Alembic for database version control
- ✅ **Testing** - Comprehensive test suite with pytest
- ✅ **Documentation** - Auto-generated OpenAPI/Swagger docs
- ✅ **Docker** - Production-ready containerization

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ (or SQLite for development)
- Redis (optional, for caching)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                 # API routes and endpoints
│   │   ├── deps.py          # Dependencies
│   │   └── v1/              # API version 1
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings
│   │   ├── security.py      # Security utilities
│   │   └── auth/            # Authentication setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic layer
│   ├── domain/              # Domain entities & interfaces
│   └── middleware/          # Custom middleware
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test types:
```bash
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m e2e          # End-to-end tests only
```

## 🔧 Development

### Code Quality

Format code:
```bash
ruff format .
```

Lint code:
```bash
ruff check .
```

Type check:
```bash
mypy app
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Security

This project implements multiple layers of security:

1. **Authentication** - FastAPI-Users with JWT tokens
2. **Authorization** - Casbin for RBAC/ABAC
3. **Data Validation** - Pydantic V2 schemas
4. **Password Security** - Bcrypt hashing
5. **CORS** - Configurable CORS policies
6. **Rate Limiting** - Request rate limiting
7. **OAuth2** - Social login support

## 🐳 Docker

Build and run with Docker:
```bash
docker-compose up --build
```

The API will be available at http://localhost:8000

## 📖 Documentation

For detailed documentation, see:

- [Architecture Specification](specification/architieve/BACKEND_ARCHITECTURE_SPECIFICATION.md)
- [Security Architecture](specification/architieve/SECURITY_ARCHITECTURE.md)
- [Code Templates](specification/architieve/CODE_TEMPLATES.md)
- [LLM Coding Guide](specification/architieve/LLM_CODING_GUIDE.md)

## 🤝 Contributing

1. Follow the Clean Architecture principles
2. Write tests for new features
3. Follow type hints conventions
4. Update documentation
5. Run linters before committing

## 📄 License

[Your License Here]

## 👥 Authors

[Your Name/Team]
