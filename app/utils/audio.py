import io
import soundfile as sf
import numpy as np
from fastapi.responses import Response

def numpy_to_wav(audio: np.ndarray, sample_rate: int) -> bytes:
    """Convert numpy array to WAV bytes"""
    buffer = io.BytesIO()
    sf.write(buffer, audio, sample_rate, format='WAV')
    return buffer.getvalue()

def create_audio_response(audio: np.ndarray, sample_rate: int) -> Response:
    """Create FastAPI response with audio"""
    wav_bytes = numpy_to_wav(audio, sample_rate)
    return Response(
        content=wav_bytes,
        media_type="audio/wav",
        headers={
            "Content-Disposition": "attachment; filename=speech.wav"
        }
    )
