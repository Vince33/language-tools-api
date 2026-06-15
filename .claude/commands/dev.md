Start the development server and open the API docs in the browser.

1. Activate the virtual environment: `source .venv/bin/activate`
2. Start the server in the background: `uvicorn main:app --reload`
3. Wait for the server to be ready (poll `http://127.0.0.1:8000/health` until it responds)
4. Use the Playwright MCP `mcp__playwright__browser_navigate` tool to open `http://127.0.0.1:8000/docs` in the browser
5. Confirm the docs page loaded and tell the user the server is running
