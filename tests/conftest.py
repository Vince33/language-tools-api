import pytest
from fastapi.testclient import TestClient
from main import app

TEST_API_KEY = "test-secret-key"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return {"X-API-Key": TEST_API_KEY}
