from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
import re
import os
import textstat
import spacy

load_dotenv()
nlp = spacy.load("en_core_web_sm")
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(_api_key_header)):
    if api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")

app = FastAPI(
    title="Language Tools API",
    description="A utility API for language detection and analysis",
    version="0.1.0",
    dependencies=[Depends(verify_api_key)],
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

class ReadabilityRequest(BaseModel):
    text: str

class ReadabilityResponse(BaseModel):
    text: str
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    reading_ease_label: str

def get_reading_ease_label(score: float) -> str:
    """Convert a Flesch Reading Ease score to a human readable label."""
    if score >= 90:
        return "Very Easy"
    elif score >= 70:
        return "Easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly Difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Very Difficult"

@app.post("/readability", response_model=ReadabilityResponse)
def analyze_readability(request: ReadabilityRequest):
    """
    Analyze the readability of the provided text.

    Returns Flesch Reading Ease score (0-100, higher is easier)
    and Flesch-Kincaid Grade Level (US school grade equivalent).
    """
    text = request.text

    flesch_ease = textstat.flesch_reading_ease(text)
    flesch_grade = textstat.flesch_kincaid_grade(text)
    label = get_reading_ease_label(flesch_ease)

    return ReadabilityResponse(
        text=text,
        flesch_reading_ease=flesch_ease,
        flesch_kincaid_grade=flesch_grade,
        reading_ease_label=label
    )

class LinguisticAnalysisRequest(BaseModel):
    text: str

class LinguisticAnalysisResponse(BaseModel):
    text: str
    average_dependency_depth: float
    lexical_diversity: float
    noun_to_verb_ratio: float

def get_dependency_depth(token):
    """Recursively calculate the depth of a token in the dependency tree."""
    if not list(token.children):
        return 1
    return 1 + max(get_dependency_depth(child) for child in token.children)

@app.post("/linguistic-analysis", response_model=LinguisticAnalysisResponse)
def linguistic_analysis(request: LinguisticAnalysisRequest):
    """
    Analyze structural linguistic properties of the provided text using spaCy.
    
    Returns average dependency tree depth (sentence structural complexity),
    lexical diversity (vocabulary variety), and noun-to-verb ratio.
    """
    text = request.text
    
    if not text.strip():
        return LinguisticAnalysisResponse(
            text=text,
            average_dependency_depth=0.0,
            lexical_diversity=0.0,
            noun_to_verb_ratio=0.0
        )
    
    doc = nlp(text)
    
    # Average dependency tree depth across sentences
    depths = []
    for sent in doc.sents:
        root = sent.root
        depths.append(get_dependency_depth(root))
    avg_depth = sum(depths) / len(depths) if depths else 0.0
    
    # Lexical diversity (type-token ratio)
    words = [token.text.lower() for token in doc if token.is_alpha]
    unique_words = set(words)
    diversity = len(unique_words) / len(words) if words else 0.0
    
    # Noun to verb ratio
    noun_count = sum(1 for token in doc if token.pos_ == "NOUN")
    verb_count = sum(1 for token in doc if token.pos_ == "VERB")
    ratio = noun_count / verb_count if verb_count > 0 else 0.0
    
    return LinguisticAnalysisResponse(
        text=text,
        average_dependency_depth=round(avg_depth, 2),
        lexical_diversity=round(diversity, 2),
        noun_to_verb_ratio=round(ratio, 2)
    )