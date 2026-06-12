from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect, LangDetectException
import re 

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
    
class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    text: str
    word_count: int
    sentence_count: int
    character_count: int
    character_count_no_spaces: int

@app.post("/analyze-text", response_model=AnalyzeResponse)
def analyze_text(request: AnalyzeRequest):
    """
    Analyze basic linguistic properties of the provided text.
    
    Returns word count, sentence count, and character counts.
    """
    text = request.text
    
    word_count = len(text.split()) if text.strip() else 0
    sentence_count = len([s for s in re.split(r'[.!?]+', text) if s.strip()]) if text.strip() else 0
    character_count = len(text)
    character_count_no_spaces = len(text.replace(" ", ""))
    
    return AnalyzeResponse(
        text=text,
        word_count=word_count,
        sentence_count=sentence_count,
        character_count=character_count,
        character_count_no_spaces=character_count_no_spaces
    )