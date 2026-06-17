import pytest
import requests


def test_linguistic_analysis_response_code_valid_input(base_url, auth_headers):
    """Valid input should return correct response code."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "The cat sat on the mat."},
        headers=auth_headers
    )
    assert response.status_code == 200

def test_linguistic_analysis_response_has_correct_structure(base_url, auth_headers):
    """Response should have the correct structure."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hello world"},
        headers=auth_headers
    )
    data = response.json()
    assert "text" in data
    assert "average_dependency_depth" in data
    assert "lexical_diversity" in data
    assert "noun_to_verb_ratio" in data

def test_linguistic_analysis_missing_text_field_returns_422(base_url, auth_headers):
    """Request with no text field should return 422 validation error."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={},
        headers=auth_headers
    )
    assert response.status_code == 422

def test_linguistic_analysis_wrong_method_returns_405(base_url):
    """GET request to POST endpoint should return 405 method not allowed."""
    response = requests.get(f"{base_url}/linguistic-analysis")
    assert response.status_code == 405
    
def test_linguistic_analysis_correct_values_known_sentence(base_url, auth_headers):
    """Known sentence should return manually verified structural values."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "The cat sat on the mat."},
        headers=auth_headers
    )
    data = response.json()
    assert data["average_dependency_depth"] == 4.0
    assert data["lexical_diversity"] == 0.83
    assert data["noun_to_verb_ratio"] == 2.0

def test_linguistic_analysis_empty_text(base_url, auth_headers):
    """Empty text should return zero counts."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": ""},
        headers=auth_headers
    )
    data = response.json()
    assert data["average_dependency_depth"] == 0.0
    assert data["lexical_diversity"] == 0.0
    assert data["noun_to_verb_ratio"] == 0.0

def test_linguistic_analysis_single_word_text(base_url, auth_headers):
    """Single word text should return correct counts."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hello"},
        headers=auth_headers
    )
    data = response.json()
    assert data["average_dependency_depth"] == 1.0
    assert data["lexical_diversity"] == 1.0
    assert data["noun_to_verb_ratio"] == 0.0

def test_linguistic_analysis_nonsense_text(base_url, auth_headers):
    """Nonsense text should return reasonable counts."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "asldkfj asldkfj asldkfj"},
        headers=auth_headers
    )
    data = response.json()
    assert isinstance(data["average_dependency_depth"], float)
    assert isinstance(data["lexical_diversity"], float)
    assert isinstance(data["noun_to_verb_ratio"], float)

def test_missing_api_key_returns_401(base_url):
    """Request with no API key should return 401."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hello world"},
    )

    assert response.status_code == 401

def test_invalid_api_key_returns_403(base_url):
    """Request with wrong API key should return 403."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hello world"},
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 403
