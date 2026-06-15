Start the server and run the full test suite.

1. Activate the virtual environment: `source .venv/bin/activate`
2. Start the server in the background: `uvicorn main:app &`
3. Wait 3 seconds for it to be ready
4. Run the tests: `pytest tests/ -v`
5. Report a summary of results — how many passed, failed, or errored, and surface any failures with their output.
