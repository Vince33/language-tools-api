import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("API_KEY")

@pytest.fixture
def auth_headers():
    return {"X-API-Key": API_KEY}

def test_server_is_up_and_responds():
    """True end-to-end smoke test - requires a live uvicorn server running."""
    response = requests.post(
        f"{BASE_URL}/analyze-text",
        json={"text": "Hello world!"},
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
