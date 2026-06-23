
def test_health_check(client, auth_headers):
    """API should return ok status for health check."""
    response = client.get("/health", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_detect_english(client, auth_headers):
    """Should correctly detect English text."""
    response = client.post(
        "/detect-language",
        json={"text": "The quick brown fox jumps over the lazy dog."},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"
    assert data["success"] == True

def test_detect_spanish(client, auth_headers):
    """Should correctly detect Spanish text."""
    response = client.post(
        "/detect-language",
        json={"text": "El rápido zorro marrón salta sobre el perro perezoso."},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "es"
    assert data["success"] == True


def test_empty_text_returns_unkown(client, auth_headers):

    """Empty text should return unknown language."""
    response = client.post(
        "/detect-language",
        json={"text": ""},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data ["language"] == "unknown"
    assert data ["success"] == False

def test_response_contains_original_text(client, auth_headers):
    """Response should echo back the original text."""
    text = "Hello, world"""
    response = client.post(
        "/detect-language",
        json={"text": text},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["text"] == text

def test_missing_text_field_returns_422(client, auth_headers):
    """Request with no text field should return 422 validation error."""
    response = client.post(
        "/detect-language",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_wrong_http_method_returns_405(client):
    """GET request to POST endpoint should return 405 method not allowed."""
    response = client.get(f"/detect-language")

    assert response.status_code == 405

def test_noneexistent_endpoint_returns_404(client):
    """Request to unkown endpoint should return 404."""
    response = client.get(f"/nonexistent")

    assert response.status_code == 404

def test_single_word_input(client, auth_headers):
    """Single word input should still return a response without crashing."""
    response = client.post(
        f"/detect-language",
        json={"text": "Hello"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "language" in data
    assert "success" in data


def test_numeric_characters_returns_response(client, auth_headers):
    """Text containing only numbers should return a resoponse without crashing."""
    response = client.post(
        "/detect-language",
        json={"text": "1234567890"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "language" in data


def test_missing_api_key_returns_401(client):
    """Request with no API key should return 401."""
    response = client.post(
        "/detect-language",
        json={"text": "Hello world"},
    )

    assert response.status_code == 401


def test_invalid_api_key_returns_403(client):
    """Request with wrong API key should return 403."""
    response = client.post(
        "/detect-language",
        json={"text": "Hello world"},
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 403
