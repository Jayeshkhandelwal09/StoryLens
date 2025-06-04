from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # AI Models
    kosmos_model_path: str = "microsoft/kosmos-2-patch14-224"
    xtts_model_path: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # File Storage
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000"
    ]
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # AI Settings
    device: str = "auto"  # auto, cpu, cuda
    max_story_length: int = 500
    audio_sample_rate: int = 22050
    audio_format: str = "wav"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name in ['cors_origins', 'allowed_extensions']:
                return [x.strip() for x in raw_val.split(',')]
            return cls.json_loads(raw_val)


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True) 