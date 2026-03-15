from pydantic import BaseModel, Field
from typing import Optional

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    voice: Optional[str] = Field("en_US-amy-medium", description="Voice model to use")
    speed: float = Field(1.0, description="Speech speed (0.5 to 2.0)")

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
