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

**GET /health**
Standard health check endpoint.

## Test structure

Tests are organized by concern across four files:

- `tests/test_detect.py` — language detection endpoint
- `tests/test_analyze.py` — text analysis endpoint  
- `tests/test_readability.py` — readability endpoint
- `tests/test_label_logic.py` — unit tests for readability label logic

Coverage follows the testing pyramid — unit tests for pure function logic, 
API tests for contract, functional, validation, and edge case layers.

## Tech stack

- Python 3.13
- FastAPI
- Pydantic
- langdetect
- textstat
- pytest

## Setup

```bash
git clone https://github.com/Vince33/language-tools-api.git
cd language-tools-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn main:app --reload
```

Interactive API documentation available at `http://127.0.0.1:8000/docs`

## Running the tests

```bash
pytest tests/ -v
```

## Status

Active — early stage. Built as a learning project alongside language-ai-qa. 
Findings and observations documented inline in test files and endpoint 
docstrings.