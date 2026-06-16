import requests

def test_readability_response_code_valid_input(base_url, auth_headers):
    """Valid input should return 200 OK."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "The cat sat on the mat."},
        headers=auth_headers,
    )

    assert response.status_code == 200

def test_readability_response_has_correct_structure(base_url, auth_headers):
    """Responnse should contain all expected fields with correct types."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "The cat sat on the mat."},
        headers=auth_headers,
    )
    data  = response.json()
    assert "text" in data
    assert "flesch_reading_ease" in data
    assert "flesch_kincaid_grade" in data
    assert isinstance(data["flesch_reading_ease"], float)
    assert isinstance(data["flesch_kincaid_grade"], float)
    assert isinstance(data["reading_ease_label"], str)

def test_readability_simple_text_is_very_easy(base_url, auth_headers):
    """Simple text should have high reading ease score and low grade level."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "The cat sat on the mat."},
        headers=auth_headers,
    )

    data = response.json()
    assert data["reading_ease_label"] == "Very Easy"

def test_readability_complex_text_is_very_difficult(base_url, auth_headers):
    """Complex text should have low reading ease score and high grade level."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "The epistemological implications of poststrucuralist discourse necessitate a fundamental reassessment of hermeneutical frameworks."},
        headers=auth_headers,
    )

    data = response.json()
    assert data["reading_ease_label"] == "Very Difficult"

def test_readability_standard_text(base_url, auth_headers):
    """Standard text should have moderate reading ease score and grade level."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "Scientists found that regular exercise helps improve memory. The study followed two hundred adults over six months. Those who exercised showed better results on memory tests."},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reading_ease_label"] == "Difficult"

def test_readability_misshing_text_field_returns_422(base_url, auth_headers):
    """Request with no text field should return 422 validation error."""
    response = requests.post(
        f"{base_url}/readability",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_readability_wrong_method_returns_405(base_url):
    """GET request to POST endpoint should return 405 method not allowed."""
    response = requests.get(f"{base_url}/readability")

    assert response.status_code == 405

def test_readability_empty_text(base_url, auth_headers):
    """Empty text should return a response without crashing."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": ""},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "reading_ease_label" in data

def test_readability_single_word_text(base_url, auth_headers):
    """Single word input should return a response without crashing"""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "Hello"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "reading_ease_label" in data

def test_readability_nonsense_text(base_url, auth_headers):
    """Nonsense text should return a response without crashing."""
    response = requests.post(
        f"{base_url}/readability",
        json={"text": "asdf asdf asdf asdf asdf"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "reading_ease_label" in data
