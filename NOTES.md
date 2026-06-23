# language-tools-api — Notes

## Finding — code coverage measures the wrong process when testing against a live server

While adding `pytest-cov` to measure test coverage, the initial report showed 
only 58% line coverage (49 of 117 statements missed), with large gaps across 
nearly every endpoint function — despite all 57 tests passing and the request 
logs clearly showing every endpoint being hit with a range of status codes 
(200, 401, 403, 422, 400).

### Root cause

The test suite runs real HTTP requests against a separately started `uvicorn` 
process (`uvicorn main:app &`), while `pytest --cov=main` only instruments 
the `pytest` process itself. Since the actual application code runs inside 
the separate server process, `coverage` never observes those lines executing 
— even though they demonstrably did, based on the request logs and passing 
assertions.

Confirmed by cross-referencing the "missing" line ranges reported against 
`main.py` — they correspond almost exactly to the bodies of `verify_api_key`, 
`detect_language`, `analyze_text`, `analyze_readability`, `get_dependency_depth`, 
and `linguistic_analysis`. All of these were exercised by the test suite; 
none of them were observed by the coverage tool.

### Why this matters

This is the same category of problem documented elsewhere in this project's 
sibling repos — a metric or tool can report an honest answer to a narrower 
question than the one you assumed it was answering. "58% covered" sounds 
like a statement about test thoroughness; it's actually an artifact of test 
architecture (out-of-process HTTP testing vs in-process testing), not a 
reflection of which code paths are genuinely exercised.

### What would fix it (now implemented)

Using FastAPI's `TestClient` to run the app in-process rather than against 
a separately started `uvicorn` server would let `coverage` observe execution 
directly. This is a meaningfully different test architecture — closer to 
unit/integration testing than the current black-box HTTP/contract-testing 
approach — and was not pursued here, since the current approach has its own 
legitimate value (testing the app exactly as a real client would call it, 
auth headers and all).

### Update — resolved

Migrated the majority of the test suite from live-server `requests` calls 
to FastAPI's `TestClient`, which runs in-process and is correctly observed 
by `coverage`. A single true end-to-end smoke test (`test_smoke.py`) was 
kept separately, requiring a live server, to preserve genuine full-stack 
verification alongside the now-accurate in-process suite.

Coverage after migration: 100%, all 119 statements in main.py, confirming 
the original 58% figure was entirely an artifact of test architecture, not 
test thoroughness.

Two real bugs surfaced during the CI migration, worth noting since they 
demonstrate why testing in a second, independent environment (not just 
locally) matters: the `API_KEY` environment variable was scoped to a 
single workflow step rather than the whole job, causing every TestClient-based 
test to fail with 403 in CI despite passing locally; and a header name typo 
(`X-API-key` instead of `X-API-Key`) in the smoke test caused it to send a 
literal string "None" as the API key. Both fixed by setting `API_KEY` at 
the job level in the GitHub Actions workflow and correcting the header name.

### Status

`.coverage` (the binary data file pytest-cov generates) added to `.gitignore`. 
Coverage tooling kept installed for future use, but the current 58% figure 
should not be read as a meaningful measure of test thoroughness given the 
out-of-process architecture.

## Design decision — empty string language treated as unspecified

While running a systematic specification-based testing pass on the 
`language` parameter for `/linguistic-analysis` (following the 
equivalence-partitioning process from Aniche's *Effective Software 
Testing*), an untested partition surfaced: `language` explicitly set to 
an empty string `""`, distinct from `language` omitted entirely or set 
to `null`.

### The question

Should `language: ""` be treated as:
- An explicit but invalid value, same as `language: "fr"` → reject with 400
- The functional equivalent of "no preference specified" → trigger auto-detection

Both are internally consistent positions. The original implementation 
took the first approach by accident — `""` simply fell into the 
`language not in SUPPORTED_LANGUAGES` check and got rejected with the 
same error as any other unsupported code.

### Decision

Treat `language: ""` as equivalent to omission, triggering auto-detection. 
Reasoning: a caller sending an explicit unsupported code like `"fr"` is 
making an active (if mistaken) request for a specific language. A caller 
sending an empty string is far more likely to have an empty form field, 
an uninitialized variable, or a default placeholder — functionally closer 
to "didn't specify anything" than "specified something wrong." Treating 
both the same way (rejecting both) would be technically defensible but 
arguably less helpful to the caller in the more common real-world case.

### Implementation

A normalization step added immediately after the empty-text guard, before 
any validation or detection logic runs:

```python
if language == "":
    language = None
```

This routes `""` into the exact same downstream path as omission or 
explicit `null`, without duplicating or branching the validation logic.

### Process note

This decision emerged from formally walking through equivalence 
partitioning on the `language` parameter — null/omitted, empty string, 
supported codes, unsupported codes — rather than from a bug report or 
manual testing. The previous test suite (58 tests, all passing) had not 
covered this partition at all; "language as empty string" was a genuine 
blind spot in test coverage despite the endpoint otherwise being 
thoroughly tested. Confirms the value of systematic partition-based 
review even on code that already has a comprehensive, passing test 
suite — passing tests only prove the cases you thought to write.
