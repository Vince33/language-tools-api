
def test_analyze_response_code_valid_input(client, auth_headers):
    """Valid input should return 200 OK."""
    response = client.post(
        "/analyze-text",
        json={"text": "Hello world. This is a test."},
        headers=auth_headers,
    )

    assert response.status_code == 200

def test_analyze_response_has_correct_structure(client, auth_headers):
    """Response should contain all expected fields with correct types."""
    response = client.post(
        "/analyze-text",
        json={"text": "Hello world. This is a test."},
        headers=auth_headers,
    )

    data = response.json()
    assert "text" in data
    assert "word_count" in data
    assert "sentence_count" in data
    assert "character_count" in data
    assert "character_count_no_spaces" in data
    assert isinstance(data["word_count"], int)
    assert isinstance(data["sentence_count"], int)
    assert isinstance(data["character_count"], int)
    assert isinstance(data["character_count_no_spaces"], int)

def test_analyze_correct_counts(client, auth_headers):
    """Counts should be correct for a known input."""
    response = client.post(
        "/analyze-text",
        json={"text": "Hello world. This is a test."},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 6  # "Hello", "world", "This", "is", "a", "test"
    assert data["sentence_count"] == 2  # "Hello world." and "This is a test."
    assert data["character_count"] == 28  # Total characters including spaces and punctuation
    assert data["character_count_no_spaces"] == 23  # Total characters excluding spaces

def test_analyze_empty_text_returns_zero_counts(client, auth_headers):
    """Empty text should return zero counts for all metrics."""
    response = client.post(
        "/analyze-text",
        json={"text": ""},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 0
    assert data["sentence_count"] == 0
    assert data["character_count"] == 0
    assert data["character_count_no_spaces"] == 0

def test_analyze_missing_text_field_returns_422(client, auth_headers):
    """Request with no text field should return 422 validation error."""
    response = client.post(
        "/analyze-text",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_analyze_numeric_text(client, auth_headers):
    """Numeric text should retrurn correct character and word counts."""
    response = client.post(
        "/analyze-text",
        json={"text": "123 456 7890"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 3  # "123", "456", "7890"
    assert data["character_count"] == 12  # 3 digits + 1 space + 3 digits + 1 space + 4 digits"
    assert data["character_count_no_spaces"] == 10  # Only digits, no spaces

def test_analyze_single_sentence_no_punctuation(client, auth_headers):
    """Text with no punctuation should count as one sentence."""
    response = client.post(
        "/analyze-text",
        json={"text": "This is a single sentence without punctuation"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentence_count"] == 1

def test_analyze_punctuation_text(client, auth_headers):
    """Text ending with ? or ! should correctly count as separate sentences."""
    response = client.post(
        "/analyze-text",
        json={"text": "How are you? I am fine!"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentence_count"] == 2

def test_missing_api_key_returns_401(client):
    """Request with no API key should return 401."""
    response = client.post(
        "/analyze-text",
        json={"text": "Hello world"},
    )

    assert response.status_code == 401

def test_invalid_api_key_returns_403(client):
    """Request with wrong API key should return 403."""
    response = client.post(
        "/analyze-text",
        json={"text": "Hello world"},
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 403