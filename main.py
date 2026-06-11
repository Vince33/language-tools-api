from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect, LangDetectException

# Create the FastAPI application instance
app = FastAPI(
    title="Language Tools API",
    description="A utility API for language detection and analysis",
    version="0.1.0"
)

# --- Request and Response Models ---
# Pydantic models define the shape of request and response data
# FastAPI uses these for automatic validation and documentation

class DetectRequest(BaseModel):
    text: str

class DetectResponse(BaseModel):
    text: str
    language: str
    success: bool

# --- Endpoints ---

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.post("/detect-language", response_model=DetectResponse)
def detect_language(request: DetectRequest):
    """
    Detect the language of the provided text.
    
    Returns the detected language code (e.g. 'en', 'es', 'fr')
    and whether detection was successful.
    """
    try:
        language = detect(request.text)
        return DetectResponse(
            text=request.text,
            language=language,
            success=True
        )
    except LangDetectException:
        return DetectResponse(
            text=request.text,
            language="unknown",
            success=False
        )