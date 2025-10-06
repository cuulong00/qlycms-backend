"""Security utilities for password hashing and JWT token management."""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify.
        hashed_password: Hashed password to verify against.
        
    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash.
        
    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create a JWT access token.
    
    Args:
        subject: Token subject (usually user ID).
        expires_delta: Token expiration time delta.
        additional_claims: Additional claims to include in token.
        
    Returns:
        str: Encoded JWT token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
    }
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def create_refresh_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT refresh token.
    
    Args:
        subject: Token subject (usually user ID).
        expires_delta: Token expiration time delta.
        
    Returns:
        str: Encoded JWT token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT token.
    
    Args:
        token: JWT token to decode.
        
    Returns:
        dict: Decoded token payload.
        
    Raises:
        JWTError: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise JWTError("Could not validate token") from e


def verify_token_type(token: str, expected_type: str) -> dict[str, Any]:
    """Verify token type (access or refresh).
    
    Args:
        token: JWT token to verify.
        expected_type: Expected token type ('access' or 'refresh').
        
    Returns:
        dict: Decoded token payload.
        
    Raises:
        JWTError: If token type doesn't match expected type.
    """
    payload = decode_token(token)
    token_type = payload.get("type")
    
    if token_type != expected_type:
        raise JWTError(
            f"Invalid token type. Expected {expected_type}, got {token_type}"
        )
    
    return payload
