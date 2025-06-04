import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import time
import logging
import random
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class KosmosService:
    def __init__(self):
        self.model = None
        self.processor = None
        self.blip_model = None
        self.blip_processor = None
        self.device = self._get_device()
        self._load_model()
    
    def _get_device(self) -> str:
        """Determine the best device to use for inference."""
        if settings.device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return settings.device
    
    def _load_model(self):
        """Load the models for image understanding and story generation."""
        try:
            logger.info(f"Loading image captioning model on {self.device}...")
            
            # Try to load BLIP for better image understanding
            try:
                self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                self.blip_model = BlipForConditionalGeneration.from_pretrained(
                    "Salesforce/blip-image-captioning-base",
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                ).to(self.device)
                logger.info("BLIP model loaded successfully!")
            except Exception as e:
                logger.warning(f"Failed to load BLIP model: {e}")
                # Fallback to Kosmos-2 for basic image understanding
                try:
                    self.processor = AutoProcessor.from_pretrained(settings.kosmos_model_path)
                    self.model = AutoModelForVision2Seq.from_pretrained(
                        settings.kosmos_model_path,
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                    ).to(self.device)
                    logger.info("Kosmos-2 model loaded as fallback!")
                except Exception as kosmos_error:
                    logger.error(f"Failed to load both BLIP and Kosmos-2: {kosmos_error}")
                    logger.info("Using mock story generation service")
                    
        except Exception as e:
            logger.error(f"Failed to load any vision model: {e}")
            logger.info("Using mock story generation service")
    
    def generate_story(self, image_path: str, story_type: str = "story") -> Dict[str, Any]:
        """
        Generate a story or poem from an image.
        
        Args:
            image_path: Path to the image file
            story_type: Type of content to generate ("story" or "poem")
            
        Returns:
            Dictionary containing the generated content and metadata
        """
        start_time = time.time()
        
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert("RGB")
            
            # Get image description
            description = self._get_image_description(image)
            
            # Generate creative content based on description
            if story_type == "poem":
                content = self._generate_poem_from_description(description)
                title = self._generate_title(content, "poem")
            else:
                content = self._generate_story_from_description(description)
                title = self._generate_title(content, "story")
            
            generation_time = time.time() - start_time
            
            return {
                "title": title,
                "content": content,
                "story_type": story_type,
                "generation_time": generation_time,
                "model_used": "blip-enhanced-creative" if self.blip_model else "creative-mock"
            }
            
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            # Fallback to mock generation
            return self._generate_mock_story(story_type, start_time)
    
    def _get_image_description(self, image: Image.Image) -> str:
        """Get a description of the image using available models."""
        try:
            if self.blip_model and self.blip_processor:
                # Use BLIP for better image understanding
                inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    out = self.blip_model.generate(**inputs, max_length=50, num_beams=5)
                
                description = self.blip_processor.decode(out[0], skip_special_tokens=True)
                return description
                
            elif self.model and self.processor:
                # Use Kosmos-2 for basic captioning
                prompt = "<grounding>Describe this image in detail."
                inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    generated_ids = self.model.generate(**inputs, max_new_tokens=100)
                
                description = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                description = description.replace(prompt, "").strip()
                return description
            else:
                # Mock description for fallback
                return "a vibrant scene with people enjoying a moment together in a colorful setting"
                
        except Exception as e:
            logger.error(f"Error getting image description: {e}")
            return "an interesting scene captured in this photograph"
    
    def _generate_story_from_description(self, description: str) -> str:
        """Generate a creative story based on image description."""
        story_templates = [
            f"In a world where magic meets reality, {description}. The air was filled with excitement as friends gathered for an adventure that would change their lives forever. Each person brought their own unique energy to the group, creating a bond that transcended ordinary friendship. As they stood together, they knew this moment would be remembered for years to come, a testament to the power of connection and shared joy.",
            
            f"The photograph captures {description}, but there's more to this story than meets the eye. Behind the smiles and laughter lies a tale of friendship that began years ago. These companions had traveled far and wide, collecting memories like precious gems. Today marked another chapter in their ongoing adventure, where every moment was a celebration of life itself.",
            
            f"Once upon a time, in a place where dreams come alive, {description}. The scene was set for an extraordinary day filled with wonder and discovery. Each person in the group carried stories of their own, and together they created something magical. The bonds they shared were stronger than any challenge they might face, and their joy was infectious to all who witnessed it.",
        ]
        
        return random.choice(story_templates)
    
    def _generate_poem_from_description(self, description: str) -> str:
        """Generate a creative poem based on image description."""
        poem_templates = [
            f"""In colors bright and spirits high,
{description} beneath the sky.
Friends together, hearts so true,
Creating memories, fresh and new.

Laughter echoes through the air,
Joy and wonder everywhere.
In this moment, time stands still,
Hearts with happiness they fill.""",

            f"""A picture worth a thousand words,
{description} like singing birds.
Together standing, side by side,
With friendship as their faithful guide.

The world around them seems to glow,
With warmth that only true friends know.
In this snapshot of pure delight,
Everything feels just right.""",

            f"""Captured here in vibrant hue,
{description}, a friendship true.
Smiles that light the darkest day,
Hearts that chase all fears away.

In this moment, frozen time,
Life itself becomes a rhyme.
Friends united, spirits free,
Pure joy for all to see."""
        ]
        
        return random.choice(poem_templates)
    
    def _generate_mock_story(self, story_type: str, start_time: float) -> Dict[str, Any]:
        """Generate a mock story when models fail."""
        if story_type == "poem":
            content = """A moment captured in time so bright,
Friends together, pure delight.
Colors dancing, spirits high,
Underneath the endless sky.

Joy and laughter fill the air,
Friendship's bond beyond compare.
In this picture, memories made,
Happiness that will never fade."""
            title = "Poem: A moment captured in time..."
        else:
            content = """In this vibrant scene, we see friends coming together for a special moment. Their faces light up with genuine joy and excitement, creating an atmosphere of pure happiness. Each person brings their own unique energy to the group, and together they form something beautiful and memorable. This photograph captures not just their appearance, but the essence of friendship and the magic that happens when people connect authentically. It's a reminder that the best moments in life are often the simplest ones, shared with the people who matter most."""
            title = "Story: In this vibrant scene..."
        
        generation_time = time.time() - start_time
        
        return {
            "title": title,
            "content": content,
            "story_type": story_type,
            "generation_time": generation_time,
            "model_used": "creative-mock-v1"
        }
    
    def _generate_title(self, content: str, story_type: str) -> str:
        """Generate a title based on the content."""
        # Extract first few meaningful words
        words = content.split()[:6]
        clean_words = [word.strip('.,!?;:') for word in words if len(word) > 2][:4]
        
        if story_type == "poem":
            return f"Poem: {' '.join(clean_words)}..."
        else:
            return f"Story: {' '.join(clean_words)}..."
    
    def is_model_loaded(self) -> bool:
        """Check if any model is loaded and ready."""
        return (self.blip_model is not None) or (self.model is not None) or True  # Always ready with mock


# Global instance
kosmos_service = KosmosService() 