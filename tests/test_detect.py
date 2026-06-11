import pytest
import requests


def test_health_check(base_url):
    """API should return ok status for health check."""
    response = requests.get(f"{base_url}/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_detect_english(base_url):
    """Should correctly detect English text."""
    response = requests.post(
        f"{base_url}/detect-language",
        json={"text": "The quick brown fox jumps over the lazy dog."}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"
    assert data["success"] == True

def test_detect_spanish(base_url):
    """Should correctly detect Spanish text."""
    response = requests.post(
        f"{base_url}/detect-language",
        json={"text": "El rápido zorro marrón salta sobre el perro perezoso."}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "es"
    assert data["success"] == True


def test_empty_text_returns_unkown(base_url):

    """Empty text should return unknown language."""
    response = requests.post(
        f"{base_url}/detect-language",
        json={"text": ""}
    )

    assert response.status_code == 200
    data = response.json()
    assert data ["language"] == "unknown"
    assert data ["success"] == False

def test_response_contains_original_text(base_url):
    """Response should echo back the original text."""
    text = "Hello, world"""
    response = requests.post(
        f"{base_url}/detect-language",
        json={"text": text}
    )

    assert response.status_code == 200
    assert response.json()["text"] == text
