"""
Imagen API Integration for Image Generation
"""
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
import time

class ImagenRenderer:
    def __init__(self):
        self.project_id = "682230388029"
        self.location = "us-central1"
        self.api_key = os.getenv("GEMINI_API_KEY", "AIzaSyAWy_LXeM7Jzve5WQ45WDHtbxssVptp7XI")
    
    def render(self, scene_data: Dict, options: Dict) -> Optional[Tuple[bytes, str]]:
        """Generate image using Imagen API"""
        try:
            # Build prompt
            prompt = self._build_prompt(scene_data, options)
            
            # Generate image
            image_bytes = self._generate_image(prompt)
            
            if not image_bytes:
                return None
            
            # Save
            output_path = self._save_image(image_bytes)
            
            return image_bytes, output_path
        
        except Exception as e:
            print(f"❌ Render Error: {e}")
            return None
    
    def _build_prompt(self, scene_data: Dict, options: Dict) -> str:
        """Build prompt from scene data"""
        space_type = options.get("space_type", "Nội thất")
        style = options.get("style", "Photorealistic")
        lighting = options.get("lighting", "natural")
        description = options.get("description", "")
        
        # Count scene elements
        meshes = len(scene_data.get("meshes", []))
        materials = len(scene_data.get("materials", []))
        
        prompt = f"Professional {space_type} design, {style} style, {lighting} lighting"
        prompt += f", {meshes} elements, {materials} materials"
        prompt += ", high quality, detailed, 4K, architectural visualization"
        
        if description:
            prompt += f", {description}"
        
        return prompt
    
    def _generate_image(self, prompt: str) -> Optional[bytes]:
        """Generate image using Imagen API"""
        try:
            from vertexai.vision_models import ImageGenerationModel
            import vertexai
            
            # Init Vertex AI
            vertexai.init(project=self.project_id, location=self.location)
            
            # Get model
            model = ImageGenerationModel.from_pretrained("imagegeneration@006")
            
            # Generate
            images = model.generate_images(
                prompt=prompt,
                number_of_images=1,
                width=1024,
                height=1024,
                safety_filter_level="block_none",
                person_generation="allow_all"
            )
            
            # Save and return bytes
            if images:
                img = images[0]
                temp_path = "/tmp/render_temp.png"
                img.save(temp_path)
                
                with open(temp_path, 'rb') as f:
                    return f.read()
            
            return None
        
        except ImportError:
            print("❌ vertexai not installed: pip install google-cloud-aiplatform")
            return None
        except Exception as e:
            print(f"Generation error: {e}")
            return None
    
    def _save_image(self, image_bytes: bytes) -> str:
        """Save image to file"""
        try:
            output_dir = Path("renders")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"render_{int(time.time())}.png"
            output_path = output_dir / filename
            
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            
            return str(output_path)
        except Exception as e:
            print(f"Save error: {e}")
            return ""
