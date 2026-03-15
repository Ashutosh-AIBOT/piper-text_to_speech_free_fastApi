import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_NAME: str = "Piper TTS API"
    API_VERSION: str = "1.0.0"
    
    # Security
    API_PASSWORD: str = os.getenv("API_PASSWORD", "default-password-change-me")
    
    # Model Settings
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "1000"))
    DEFAULT_VOICE: str = os.getenv("DEFAULT_VOICE", "en_US-amy-medium")
    SAMPLE_RATE: int = 22050
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 7860

settings = Settings()
