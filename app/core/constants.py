"""Application constants."""

from enum import Enum


class Environment(str, Enum):
    """Application environment types."""
    
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class UserRole(str, Enum):
    """User role types for RBAC."""
    
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Permission(str, Enum):
    """Permission types for access control."""
    
    # User permissions
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    
    # Item permissions
    ITEM_READ = "item:read"
    ITEM_WRITE = "item:write"
    ITEM_DELETE = "item:delete"
    
    # Admin permissions
    ADMIN_READ = "admin:read"
    ADMIN_WRITE = "admin:write"
    ADMIN_DELETE = "admin:delete"


class TokenType(str, Enum):
    """JWT token types."""
    
    ACCESS = "access"
    REFRESH = "refresh"


class HTTPMethod(str, Enum):
    """HTTP methods."""
    
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


# API Configuration
API_V1_PREFIX = "/api/v1"
API_V2_PREFIX = "/api/v2"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 60
RATE_LIMIT_PER_HOUR = 1000

# Cache TTL (seconds)
CACHE_TTL_SHORT = 60  # 1 minute
CACHE_TTL_MEDIUM = 300  # 5 minutes
CACHE_TTL_LONG = 3600  # 1 hour

# File Upload
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_UPLOAD_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx"}

# Database
MAX_QUERY_LIMIT = 1000
DEFAULT_QUERY_LIMIT = 100

# Security
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

# OAuth2
OAUTH_STATE_LENGTH = 32
OAUTH_CALLBACK_PATH = "/auth/oauth/callback"

# Logging
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MESSAGE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
