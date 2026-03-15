from fastapi import APIRouter, Depends, HTTPException
import logging

from app.schemas.requests import TTSRequest
from app.models.piper import PiperModel
from app.api.dependencies import verify_password
from app.utils.audio import create_audio_response
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Global model instance (loaded once at startup)
model = None

@router.on_event("startup")
async def startup_event():
    """Load model when API starts"""
    global model
    model = PiperModel()
    await model.load()

@router.on_event("shutdown")
async def shutdown_event():
    """Unload model when API stops"""
    global model
    if model:
        await model.unload()

@router.post("/v1/tts")
async def text_to_speech(
    request: TTSRequest,
    auth=Depends(verify_password)
):
    """
    Convert text to speech using Piper TTS
    
    - **text**: Text to convert (max 1000 chars)
    - **voice**: Voice model (default: en_US-amy-medium)
    - **speed**: Speech speed (0.5-2.0)
    """
    global model
    
    if not model or not model.is_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Try again in a moment."
        )
    
    try:
        # Validate text length
        if len(request.text) > settings.MAX_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Max {settings.MAX_TEXT_LENGTH} characters"
            )
        
        # Generate audio
        audio = await model.synthesize(
            text=request.text,
            voice=request.voice,
            speed=request.speed
        )
        
        # Return audio file
        return create_audio_response(audio, model.sample_rate)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate speech"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    global model
    return {
        "status": "healthy",
        "model_loaded": model.is_loaded if model else False,
        "max_text_length": settings.MAX_TEXT_LENGTH
    }

@router.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Piper TTS API",
        "version": "1.0.0",
        "endpoints": {
            "POST /v1/tts": "Convert text to speech",
            "GET /health": "Health check"
        },
        "docs": "/docs"
    }
