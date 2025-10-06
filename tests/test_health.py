"""Test health check endpoints."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


def test_ping(client: TestClient) -> None:
    """Test ping endpoint."""
    response = client.get("/api/v1/health/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
