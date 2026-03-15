from abc import ABC, abstractmethod
import numpy as np
from typing import Optional

class BaseTTSModel(ABC):
    """Abstract base class for all TTS models"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_loaded = False
        self.sample_rate = 22050
    
    @abstractmethod
    async def load(self) -> bool:
        """Load the model into memory"""
        pass
    
    @abstractmethod
    async def synthesize(self, text: str, voice: Optional[str] = None, 
                        speed: float = 1.0) -> np.ndarray:
        """Convert text to speech"""
        pass
    
    @abstractmethod
    async def unload(self) -> bool:
        """Unload model from memory"""
        pass
    
    def validate_text(self, text: str) -> bool:
        """Validate input text"""
        from app.config import settings
        return bool(text) and len(text) <= settings.MAX_TEXT_LENGTH
