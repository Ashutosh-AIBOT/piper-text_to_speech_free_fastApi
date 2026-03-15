import numpy as np
import soundfile as sf
import io
import logging
from pathlib import Path
import tempfile
import subprocess
import os

from .base import BaseTTSModel

logger = logging.getLogger(__name__)

class PiperModel(BaseTTSModel):
    """Piper TTS model implementation"""
    
    def __init__(self):
        super().__init__("piper-tts")
        self.model_path = None
        self.sample_rate = 22050
    
    async def load(self) -> bool:
        """Download and load Piper model"""
        try:
            logger.info("Loading Piper TTS model...")
            
            # Create models directory
            models_dir = Path.home() / ".piper"
            models_dir.mkdir(exist_ok=True)
            
            # Check if model already exists
            model_file = models_dir / "en_US-amy-medium.onnx"
            config_file = models_dir / "en_US-amy-medium.onnx.json"
            
            if not model_file.exists():
                logger.info("Downloading Piper model...")
                # Download model using piper CLI
                subprocess.run([
                    "piper", "download", "en_US-amy-medium"
                ], check=True)
            
            self.model_path = str(model_file)
            self.is_loaded = True
            logger.info("✅ Piper model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Piper model: {e}")
            return False
    
    async def synthesize(self, text: str, voice: str = "en_US-amy-medium", 
                        speed: float = 1.0) -> np.ndarray:
        """Generate speech from text"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        if not self.validate_text(text):
            raise ValueError("Invalid text input")
        
        # Create temp file for output
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            # Run piper to generate audio
            process = subprocess.run([
                "echo", text, "|", "piper",
                "--model", voice,
                "--output_file", output_path,
                "--length_scale", str(1.0 / speed)
            ], shell=True, capture_output=True, text=True)
            
            if process.returncode != 0:
                raise RuntimeError(f"Piper failed: {process.stderr}")
            
            # Read audio file
            audio, sr = sf.read(output_path)
            
            # Resample if needed
            if sr != self.sample_rate:
                # Simple resampling (for demo)
                audio = np.interp(
                    np.linspace(0, len(audio), int(len(audio) * self.sample_rate / sr)),
                    np.arange(len(audio)),
                    audio
                )
            
            return audio.astype(np.float32)
            
        finally:
            # Cleanup temp file
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    async def unload(self) -> bool:
        """Unload model (Piper is stateless, so just set flag)"""
        self.is_loaded = False
        return True
