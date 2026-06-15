# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (required before running anything)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server (reload on file changes)
uvicorn main:app --reload

# Run all tests (server must be running first)
pytest tests/ -v

# Run a single test file
pytest tests/test_detect.py -v

# Run a single test by name
pytest tests/test_label_logic.py::test_label_returns_very_easy_for_high_score -v
```

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the server is running.

## Architecture

The entire API lives in a single file: `main.py`. There are no routers, services, or modules — each endpoint is a standalone function with its Pydantic request/response models defined inline above it.

**Endpoints:**
- `GET /health` — liveness check
- `POST /detect-language` — language code detection via `langdetect`
- `POST /analyze-text` — word/sentence/character counts using regex splitting on `[.!?]+`
- `POST /readability` — Flesch Reading Ease + Flesch-Kincaid Grade via `textstat`, plus a label from `get_reading_ease_label()`

`get_reading_ease_label()` is the only pure function extracted from an endpoint, and it has its own unit test file (`tests/test_label_logic.py`) that imports it directly from `main`.

## Test structure

Tests are split into two layers:

1. **API tests** (`test_detect.py`, `test_analyze.py`, `test_readability.py`) — hit a live server over HTTP using `requests`. The `base_url` fixture in `conftest.py` supplies `http://127.0.0.1:8000`. These tests require the server to be running before `pytest` is invoked.

2. **Unit tests** (`test_label_logic.py`) — import and call `get_reading_ease_label` directly, no server needed.

CI (`.github/workflows/tests.yml`) starts the server with `uvicorn main:app &` and waits 3 seconds before running `pytest`.

## Known behaviors

- Flesch scores can legitimately fall outside 0–100 for very simple or very complex text — this is expected formula behavior.
- `langdetect` detection quality degrades on short or ambiguous input; single-word tests assert only that a response is returned, not the specific language.
