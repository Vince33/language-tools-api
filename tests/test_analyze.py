import requests

def test_analyze_response_code_valid_input(base_url):
    """Valid input should return 200 OK."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": "Hello world. This is a test."}
    )

    assert response.status_code == 200

def test_analyze_response_has_correct_structure(base_url):
    """Response should contain all expected fields with correct types."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": "Hello world. This is a test."}
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

def test_analyze_correct_counts(base_url):
    """Counts should be correct for a known input."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": "Hello world. This is a test."}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 6  # "Hello", "world", "This", "is", "a", "test"
    assert data["sentence_count"] == 2  # "Hello world." and "This is a test."
    assert data["character_count"] == 28  # Total characters including spaces and punctuation
    assert data["character_count_no_spaces"] == 23  # Total characters excluding spaces

def test_analyze_empty_text_returns_zero_counts(base_url):
    """Empty text should return zero counts for all metrics."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": ""}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 0
    assert data["sentence_count"] == 0
    assert data["character_count"] == 0
    assert data["character_count_no_spaces"] == 0

def test_analyze_missing_text_field_returns_422(base_url):
    """Request with no text field should return 422 validation error."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={}
    )

    assert response.status_code == 422

def test_analyze_numeric_text(base_url):
    """Numeric text should retrurn correct character and word counts."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": "123 456 7890"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 3  # "123", "456", "7890"
    assert data["character_count"] == 12  # 3 digits + 1 space + 3 digits + 1 space + 4 digits"
    assert data["character_count_no_spaces"] == 10  # Only digits, no spaces

def test_analyze_single_sentence_no_punctuation(base_url):
    """Text with no punctuation should count as one sentence."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": "This is a single sentence without punctuation"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentence_count"] == 1

def test_analyze_punctuation_text(base_url):
    """Text ending with ? or ! should correctly count as separate sentences."""
    response = requests.post(
        f"{base_url}/analyze-text",
        json={"text": "How are you? I am fine!"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentence_count"] == 2
    