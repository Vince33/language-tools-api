# language-tools-api

A lightweight Python API for language detection and text analysis, built 
as a learning project exploring Python API development and test automation 
practices.

## What this is

A REST API that provides language utility endpoints — detecting the language 
of text, analyzing basic linguistic properties, and scoring readability using 
established linguistic formulas. Built alongside language-ai-qa as a companion 
project focused on developing Python API development and structured test 
automation skills.

The readability scoring connects directly to language acquisition research — 
Flesch-Kincaid grade level scoring is a quantitative measure of text 
complexity, relevant to comprehensible input theory and language learning 
contexts.

## Authentication

All endpoints require an API key passed in the `X-API-Key` request header.

```
X-API-Key: your-api-key
```

Set the key server-side via the `API_KEY` environment variable. Requests with 
a missing key return `401`; requests with an incorrect key return `403`.

## Endpoints

**POST /detect-language**
Detects the language of provided text using langdetect. Returns the detected 
language code and whether detection succeeded. Known limitation: detection 
quality degrades significantly on short text and is unreliable for low-resource 
languages not represented in langdetect's training data.

**POST /analyze-text**
Returns basic linguistic properties of provided text — word count, sentence 
count, character count with and without spaces. Sentence detection handles 
period, question mark, and exclamation point delimiters.

**POST /readability**
Returns Flesch Reading Ease score and Flesch-Kincaid Grade Level for provided 
text, along with a human-readable difficulty label. Scores can exceed the 
standard 0-100 range for very simple or very complex text — this is expected 
behavior of the formula, not an error.

**POST /linguistic-analysis**
Returns structural linguistic properties of provided text using spaCy — 
average dependency tree depth (sentence structural complexity), lexical 
diversity (type-token ratio), and noun-to-verb ratio. These are exploratory 
structural signals, not a calibrated composite score like Flesch-Kincaid.

Supports English and Spanish. An optional `language` field accepts `en` or 
`es`; if omitted, the language is auto-detected. An explicit `language` value 
outside the supported set, or auto-detected text in an unsupported language, 
returns a `400` error rather than silently defaulting — nothing is guessed 
without telling the caller. Empty text returns `language: null` along with 
zeroed metrics, since no language can be determined from nothing.

**GET /health**
Standard health check endpoint.

## Test structure

Tests are organized by concern across four files:

- `tests/test_detect.py` — language detection endpoint
- `tests/test_analyze.py` — text analysis endpoint  
- `tests/test_readability.py` — readability endpoint
- `tests/test_label_logic.py` — unit tests for readability label logic
- `tests/test_linguistic_analysis.py` — linguistic analysis endpoint

Coverage follows the testing pyramid — unit tests for pure function logic, 
API tests for contract, functional, validation, and edge case layers.

## Testing with Postman

A Postman collection is included in the repository (`postman_collection.json`) with pre-built requests for all API endpoints. Import it into Postman to manually test and explore the API without writing any code.

## Development tooling

[Claude Code](https://claude.ai/code) is used as a development assistant throughout this project — for generating and refining tests, exploring endpoint behavior, and iterating on implementation. Custom commands for common tasks are available in `.claude/commands/`.

## Tech stack

- Python 3.13
- FastAPI
- Pydantic
- langdetect
- textstat
- pytest
- spaCy

## Setup

```bash
git clone https://github.com/Vince33/language-tools-api.git
cd language-tools-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the server

Copy `.env.example` to `.env` and set your key:

```bash
cp .env.example .env
# edit .env and set API_KEY=your-api-key
uvicorn main:app --reload
```

Interactive API documentation available at `http://127.0.0.1:8000/docs`

## Running the tests

Most tests use FastAPI's TestClient and run in-process — no server needs 
to be running first.

```bash
pytest tests/ -v
```

One test (`tests/test_smoke.py`) is a true end-to-end smoke test and 
requires a live server running with `API_KEY` set:

```bash
export API_KEY=test-secret-key
uvicorn main:app &
pytest tests/test_smoke.py -v
```

## Status

Active — early stage. Built as a learning project alongside language-ai-qa. 
Findings and observations documented inline in test files and endpoint 
docstrings.