from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.tts_service import tts_service
from app.services.file_service import file_service
from pydantic import BaseModel
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()


class AudioGenerationRequest(BaseModel):
    text: str
    voice: str = "default"


class AudioResponse(BaseModel):
    audio_filename: str
    audio_path: str
    generation_time: float
    duration: float
    model_used: str
    message: str


@router.post("/audio/generate", response_model=AudioResponse)
async def generate_audio(request: AudioGenerationRequest):
    """
    Generate audio narration from text.
    
    Args:
        request: Audio generation request with text and voice preference
    
    Returns:
        Audio generation result with metadata
    """
    try:
        # Generate unique filename for audio
        import time
        audio_filename = f"audio_{int(time.time())}.{file_service.audio_format}"
        audio_path = file_service.get_audio_path(audio_filename)
        
        # Generate audio using TTS service
        audio_result = tts_service.generate_audio(
            text=request.text,
            output_path=audio_path,
            voice=request.voice
        )
        
        return AudioResponse(
            audio_filename=audio_filename,
            audio_path=audio_path,
            generation_time=audio_result["generation_time"],
            duration=audio_result.get("duration", 0),
            model_used=audio_result["model_used"],
            message="Audio generated successfully!"
        )
        
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate audio")


@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Get audio file by filename.
    
    Args:
        filename: Name of the audio file
    
    Returns:
        Audio file response
    """
    try:
        audio_path = file_service.get_audio_path(filename)
        
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            path=audio_path,
            media_type="audio/wav",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving audio file {filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to serve audio file")


@router.delete("/audio/{filename}")
async def delete_audio(filename: str):
    """
    Delete audio file by filename.
    
    Args:
        filename: Name of the audio file to delete
    
    Returns:
        Success message
    """
    try:
        audio_path = file_service.get_audio_path(filename)
        
        if file_service.delete_file(audio_path):
            return {"message": "Audio deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Audio file not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting audio file {filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete audio")


@router.get("/audio/status/tts")
async def get_tts_status():
    """Get the status of the TTS service."""
    return {
        "tts_model_loaded": tts_service.is_model_loaded(),
        "available_voices": tts_service.get_available_voices(),
        "model_name": "xtts-v2"
    } 