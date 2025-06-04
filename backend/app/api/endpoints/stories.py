from fastapi import APIRouter, HTTPException
import logging
import os
from app.services.file_service import file_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stories/stats/summary")
async def get_stories_stats():
    """
    Get basic statistics about uploaded files.
    
    Returns:
        Basic file statistics
    """
    try:
        # Get storage stats from file service
        storage_stats = file_service.get_storage_stats()
        
        # Count image files in upload directory
        images_dir = os.path.join(file_service.upload_dir, "images")
        audio_dir = os.path.join(file_service.upload_dir, "audio")
        
        image_count = 0
        audio_count = 0
        
        if os.path.exists(images_dir):
            image_count = len([f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        
        if os.path.exists(audio_dir):
            audio_count = len([f for f in os.listdir(audio_dir) if f.lower().endswith('.wav')])
        
        return {
            "total_images": image_count,
            "total_audio_files": audio_count,
            "total_size_mb": storage_stats.get("total_size_mb", 0),
            "upload_dir": storage_stats.get("upload_dir", ""),
            "message": "File-based storage statistics"
        }
        
    except Exception as e:
        logger.error(f"Error getting file stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics") 