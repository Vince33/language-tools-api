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
        json={"text": "The cat sat on the mat."},
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

def test_linguistic_analysis_null_text_returns_422(base_url, auth_headers):
    """Request with text explicitly set to null should return 422."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": None},
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
        json={"text": "Hello","language": "en"},
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
        json={"text": "asldkfj asldkfj asldkfj","language": "en"},
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

def test_unsupported_language_returns_400(base_url, auth_headers):
    """Request with unsupported language should return 400."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hello world", "language": "fr"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert "Unsupported language: 'fr'" in response.json().get("detail", "")

def test_auto_detect_unsupported_language_returns_400(base_url, auth_headers):
    """Request with auto-detected unsupported language should return 400."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Bonjour le monde"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert "Detected language 'fr' is not supported" in response.json().get("detail", "")

def test_explicitly_specified_spanish_language_returns_language_code_and_200(base_url, auth_headers):
    """Request with explicitly specified Spanish language should return 200."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hola mundo", "language": "es"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "es"

def test_auto_detect_spanish_language_returns_language_code_and_200(base_url, auth_headers):
    """Request with Spanish text should auto-detect language and return 200."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "El gato se sentó en la alfombra."},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "es"

def test_auto_detect_english_language_returns_language_code_and_200(base_url, auth_headers):
    """Request with English text should auto-detect language and return 200."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "The cat sat on the mat."},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"
    
def test_empty_string_language_triggers_auto_detection(base_url, auth_headers):
    """Empty string language should be treated as unspecified, triggering auto-detection."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "This is a test sentence for auto detection.", "language": ""},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"

def test_explicitly_specified_english_language_returns_language_code_and_200(base_url, auth_headers):
    """Request with explicitly specified English language should return 200."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": "Hello world", "language": "en"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"

def test_empty_text_returns_language_none(base_url, auth_headers):
    """Request with empty text should return language as None."""
    response = requests.post(
        f"{base_url}/linguistic-analysis",
        json={"text": ""},
        headers=auth_headers,
    )


    assert response.status_code == 200
    data = response.json()
    assert data["language"] is None

