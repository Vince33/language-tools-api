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

### What would fix it (not implemented)

Using FastAPI's `TestClient` to run the app in-process rather than against 
a separately started `uvicorn` server would let `coverage` observe execution 
directly. This is a meaningfully different test architecture — closer to 
unit/integration testing than the current black-box HTTP/contract-testing 
approach — and was not pursued here, since the current approach has its own 
legitimate value (testing the app exactly as a real client would call it, 
auth headers and all).

### Status

`.coverage` (the binary data file pytest-cov generates) added to `.gitignore`. 
Coverage tooling kept installed for future use, but the current 58% figure 
should not be read as a meaningful measure of test thoroughness given the 
out-of-process architecture.