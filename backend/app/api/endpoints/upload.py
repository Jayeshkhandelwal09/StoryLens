from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import file_service
from app.services.kosmos_service import kosmos_service
import logging
import time

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    story_type: str = "story"
):
    """
    Upload an image and generate a story or poem.
    
    Args:
        file: Image file to upload
        story_type: Type of content to generate ("story" or "poem")
    
    Returns:
        Generated story with metadata
    """
    try:
        # Validate story type
        if story_type not in ["story", "poem"]:
            raise HTTPException(status_code=400, detail="story_type must be 'story' or 'poem'")
        
        # Save uploaded file
        file_info = await file_service.save_uploaded_image(file)
        
        try:
            # Generate story using Kosmos-2
            story_data = kosmos_service.generate_story(
                image_path=file_info["path"],
                story_type=story_type
            )
            
            # Create response with generated story
            response = {
                "id": int(time.time()),  # Simple ID based on timestamp
                "title": story_data["title"],
                "content": story_data["content"],
                "story_type": story_data["story_type"],
                "image_filename": file_info["filename"],
                "image_path": file_info["path"],
                "generation_time": story_data["generation_time"],
                "model_used": story_data["model_used"],
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "message": "Story generated successfully!"
            }
            
            return response
            
        except Exception as e:
            # Clean up uploaded file if story generation fails
            file_service.delete_file(file_info["path"])
            logger.error(f"Error generating story: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate story from image")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/upload/status")
async def get_upload_status():
    """Get the status of AI models and upload service."""
    return {
        "kosmos_model_loaded": kosmos_service.is_model_loaded(),
        "max_file_size": file_service.max_file_size,
        "allowed_extensions": file_service.allowed_extensions,
        "upload_dir": file_service.upload_dir
    } 