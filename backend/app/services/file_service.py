import os
import uuid
import shutil
from typing import Optional, List, Dict, Any
from fastapi import UploadFile, HTTPException
from PIL import Image
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
        self.upload_dir = settings.upload_dir
        self.max_file_size = settings.max_file_size
        self.allowed_extensions = settings.allowed_extensions
        self.audio_format = settings.audio_format
        
        # Create subdirectories
        self.images_dir = os.path.join(self.upload_dir, "images")
        self.audio_dir = os.path.join(self.upload_dir, "audio")
        
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def validate_image_file(self, file: UploadFile) -> bool:
        """Validate uploaded image file."""
        # Check file size
        if hasattr(file, 'size') and file.size > self.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {self.max_file_size} bytes"
            )
        
        # Check file extension
        if file.filename:
            extension = file.filename.split('.')[-1].lower()
            if extension not in self.allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
                )
        
        return True
    
    async def save_uploaded_image(self, file: UploadFile) -> Dict[str, str]:
        """Save uploaded image file and return file info."""
        try:
            # Validate file
            self.validate_image_file(file)
            
            # Generate unique filename
            file_extension = file.filename.split('.')[-1].lower() if file.filename else 'jpg'
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(self.images_dir, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Validate and process image
            try:
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                        img.save(file_path, 'JPEG', quality=95)
                        unique_filename = unique_filename.replace(f'.{file_extension}', '.jpg')
                        new_path = os.path.join(self.images_dir, unique_filename)
                        os.rename(file_path, new_path)
                        file_path = new_path
                    
                    # Get image dimensions
                    width, height = img.size
                    
            except Exception as e:
                # Clean up invalid file
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=400, detail="Invalid image file")
            
            return {
                "filename": unique_filename,
                "path": file_path,
                "size": os.path.getsize(file_path),
                "width": width,
                "height": height
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving uploaded file: {e}")
            raise HTTPException(status_code=500, detail="Failed to save uploaded file")
    
    def get_audio_path(self, filename: str) -> str:
        """Get full path for audio file."""
        return os.path.join(self.audio_dir, filename)
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file safely."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get information about a file."""
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return {
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime,
                    "exists": True
                }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
        
        return {"exists": False}
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage usage statistics."""
        try:
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(self.upload_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                    except:
                        continue
            
            return {
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_count": file_count,
                "upload_dir": self.upload_dir
            }
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return {"error": str(e)}


# Global instance
file_service = FileService() 