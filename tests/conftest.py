import pytest

TEST_API_KEY = "test-secret-key"

@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"

@pytest.fixture
def auth_headers():
    return {"X-API-Key": TEST_API_KEY}
