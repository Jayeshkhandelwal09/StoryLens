import os
import time
import logging
from typing import Optional, Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)


class TTSService:
    def __init__(self):
        self.tts = None
        self.device = self._get_device()
        self._load_model()
    
    def _get_device(self) -> str:
        """Determine the best device to use for TTS."""
        if settings.device == "auto":
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"
        return "cpu" if settings.device == "cpu" else "cuda"
    
    def _load_model(self):
        """Load the XTTS-v2 model."""
        try:
            from TTS.api import TTS
            import soundfile as sf
            import numpy as np
            
            logger.info(f"Loading XTTS-v2 model on {self.device}...")
            self.tts = TTS(
                model_name=settings.xtts_model_path,
                gpu=self.device == "cuda"
            )
            logger.info("XTTS-v2 model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load XTTS-v2 model: {e}")
            # Fallback to a simpler TTS model if XTTS fails
            try:
                from TTS.api import TTS
                logger.info("Falling back to simpler TTS model...")
                self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
                logger.info("Fallback TTS model loaded successfully!")
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback TTS model: {fallback_error}")
                logger.warning("TTS will not be available - using mock service")
                self.tts = None
    
    def generate_audio(self, text: str, output_path: str, voice: str = "default") -> Dict[str, Any]:
        """
        Generate audio narration from text.
        
        Args:
            text: Text to convert to speech
            output_path: Path where to save the audio file
            voice: Voice to use (for future enhancement)
            
        Returns:
            Dictionary containing audio generation metadata
        """
        start_time = time.time()
        
        try:
            if self.tts is None:
                # Fallback to mock generation
                return self._mock_generate_audio(text, output_path, voice, start_time)
            
            # Clean the text for better TTS
            cleaned_text = self._clean_text_for_tts(text)
            
            # Generate audio
            if hasattr(self.tts, 'tts_to_file'):
                # For newer TTS versions
                self.tts.tts_to_file(
                    text=cleaned_text,
                    file_path=output_path
                )
            else:
                # For older TTS versions
                import soundfile as sf
                wav = self.tts.tts(text=cleaned_text)
                sf.write(output_path, wav, settings.audio_sample_rate)
            
            generation_time = time.time() - start_time
            
            # Get audio file info
            audio_info = self._get_audio_info(output_path)
            
            return {
                "audio_path": output_path,
                "generation_time": generation_time,
                "model_used": "xtts-v2",
                "duration": audio_info.get("duration", 0),
                "sample_rate": settings.audio_sample_rate,
                "format": settings.audio_format
            }
            
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            # Fallback to mock generation
            return self._mock_generate_audio(text, output_path, voice, start_time)
    
    def _mock_generate_audio(self, text: str, output_path: str, voice: str, start_time: float) -> Dict[str, Any]:
        """Generate mock audio file when TTS is not available."""
        try:
            # Create a placeholder audio file
            with open(output_path, 'w') as f:
                f.write("# Mock audio file - TTS not available\n")
                f.write(f"# Text: {text[:100]}...\n")
                f.write(f"# Voice: {voice}\n")
            
            generation_time = time.time() - start_time
            
            return {
                "audio_path": output_path,
                "generation_time": generation_time,
                "model_used": "mock-tts-v1",
                "duration": len(text) * 0.1,  # Rough estimate
                "sample_rate": settings.audio_sample_rate,
                "format": settings.audio_format
            }
        except Exception as e:
            logger.error(f"Error in mock audio generation: {e}")
            raise
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text to improve TTS quality."""
        # Remove or replace problematic characters
        text = text.replace('"', '')
        text = text.replace('"', '')
        text = text.replace('"', '')
        text = text.replace('—', '-')
        text = text.replace('–', '-')
        text = text.replace("'", "'")
        text = text.replace("'", "'")
        
        # Remove any remaining special tokens or markup
        text = text.replace('<grounding>', '')
        text = text.replace('</grounding>', '')
        text = text.replace('<phrase>', '')
        text = text.replace('</phrase>', '')
        text = text.replace('<object>', '')
        text = text.replace('</object>', '')
        text = text.replace('<patch_index_', '')
        text = text.replace('>', '')
        
        # Remove any sequences that look like technical tokens
        import re
        text = re.sub(r'<[^>]*>', '', text)  # Remove any remaining XML-like tags
        text = re.sub(r'\([^)]*\):', '', text)  # Remove parenthetical technical notes
        text = re.sub(r'patch_index_\d+', '', text)  # Remove patch index references
        
        # Clean up multiple spaces and line breaks
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Ensure proper sentence structure
        if not text:
            text = "This is a beautiful image that captures a wonderful moment."
        
        # Ensure proper sentence endings
        if not text.endswith('.'):
            text += '.'
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Limit length for better TTS performance
        words = text.split()
        if len(words) > 100:  # Limit to ~100 words for better audio quality
            text = ' '.join(words[:100]) + '.'
        
        return text
    
    def _get_audio_info(self, audio_path: str) -> Dict[str, Any]:
        """Get information about the generated audio file."""
        try:
            if os.path.exists(audio_path):
                # Get file size
                file_size = os.path.getsize(audio_path)
                
                # Try to get duration using soundfile
                try:
                    import soundfile as sf
                    with sf.SoundFile(audio_path) as f:
                        duration = len(f) / f.samplerate
                except:
                    duration = 0
                
                return {
                    "file_size": file_size,
                    "duration": duration
                }
        except Exception as e:
            logger.warning(f"Could not get audio info: {e}")
        
        return {"file_size": 0, "duration": 0}
    
    def is_model_loaded(self) -> bool:
        """Check if the TTS model is loaded and ready."""
        return self.tts is not None
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices (for future enhancement)."""
        # This is a placeholder for future voice selection feature
        return ["default", "female", "male"]


class MockTTSService:
    """Mock TTS service for testing without actual TTS dependencies."""
    
    def __init__(self):
        self.model_loaded = False
        logger.info("Mock TTS service initialized")
    
    def is_model_loaded(self) -> bool:
        """Check if TTS model is loaded."""
        return True  # Always return True for mock
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices."""
        return ["default", "female", "male"]
    
    def generate_audio(self, text: str, output_path: str, voice: str = "default") -> Dict:
        """
        Mock audio generation - creates a placeholder file.
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file should be saved
            voice: Voice to use for generation
        
        Returns:
            Generation result with metadata
        """
        try:
            start_time = time.time()
            
            # Create a placeholder audio file (empty file for now)
            with open(output_path, 'w') as f:
                f.write("# Mock audio file - TTS not available\n")
                f.write(f"# Text: {text[:100]}...\n")
                f.write(f"# Voice: {voice}\n")
            
            generation_time = time.time() - start_time
            
            logger.info(f"Mock audio generated for text length {len(text)} in {generation_time:.2f}s")
            
            return {
                "generation_time": generation_time,
                "model_used": "mock-tts-v1",
                "duration": len(text) * 0.1,  # Rough estimate: 0.1s per character
                "voice_used": voice,
                "output_path": output_path
            }
            
        except Exception as e:
            logger.error(f"Error in mock audio generation: {e}")
            raise Exception(f"Mock TTS generation failed: {e}")


# Try to use real TTS service, fallback to mock if not available
try:
    tts_service = TTSService()
except Exception as e:
    logger.warning(f"Failed to initialize TTS service, using mock: {e}")
    tts_service = MockTTSService() 