"""
Image Generator Module
Handles image generation using Replicate API.
"""

import requests
import time
from typing import Optional
from config import Config
from datetime import datetime
import os


class ImageGenerator:
    """Generator for images using Replicate API."""
    
    def __init__(self):
        """Initialize Image generator."""
        self.api_token = Config.REPLICATE_API_TOKEN
        self.api_base = "https://api.replicate.com/v1"
        self.timeout = 120  # seconds - image generation can take longer
        self.history_file = "image_generation_history.txt"
        self.images_dir = "images"
        
        # Create images directory if it doesn't exist
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    def _extract_theme_from_post(self, post: str) -> str:
        """
        Extract the main theme from the LinkedIn post.
        
        Args:
            post: The LinkedIn post text
            
        Returns:
            A brief theme description
        """
        # Try to extract the first line or title
        lines = post.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            # Remove common title markers
            for marker in ['#', '**', 'Título:', 'Title:']:
                if first_line.startswith(marker):
                    first_line = first_line[len(marker):].strip()
            return first_line[:100]  # Limit to 100 characters
        return "business and technology"
    
    def generate_image(self, post: str) -> str:
        """
        Generate an image based on the LinkedIn post using Replicate API.
        
        Args:
            post: The LinkedIn post text
            
        Returns:
            The image URL as a string
        """
        if not post:
            return "No post content available for image generation."
        
        if not self.api_token:
            return "Erro: REPLICATE_API_TOKEN não configurado. Adicione ao arquivo .env"
        
        # Extract theme from post
        theme = self._extract_theme_from_post(post)
        
        # Build the prompt for image generation
        prompt = f"""Editorial-style conceptual image representing: {theme}.

            No text.
            No logos.
            No peoples.
            No corporate stock-photo look.

            Professional, thought-provoking.
            Designed to stop scrolling and provoke reflection."""
        
        # Implement exponential backoff for rate limiting
        max_retries = 3
        base_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                # Add small delay before request to avoid rate limit
                if attempt > 0:
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limit detected. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(delay)
                else:
                    # Initial small delay for first request
                    time.sleep(0.5)
                
                # Build the request
                url = f"{self.api_base}/predictions"
                headers = {
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                    "Prefer": "wait"
                }
                
                payload = {
                    "version": "black-forest-labs/flux-dev",
                    "input": {
                        "prompt": prompt,
                        "aspect_ratio": "1:1",
                        "num_outputs": 1,
                        "num_inference_steps": 32,
                        "guidance": 3.2,
                        "megapixels": "1",
                        "output_format": "webp",
                        "output_quality": 80,
                        "go_fast": True
                    }
                }
                
                print(f"DEBUG: Sending image generation request to {url}")
                print(f"DEBUG: Prompt: {prompt[:100]}...")
                
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                print(f"DEBUG: Response status code: {response.status_code}")
                
                # Check for rate limit error
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        # Will retry in next iteration with exponential backoff
                        continue
                    else:
                        return "Erro: Limite de taxa da API excedido. Tente novamente em alguns minutos."
                
                response.raise_for_status()
                result = response.json()
                
                print(f"DEBUG: Response: {result}")
                
                # Extract image URL from response
                image_url = ""
                if "output" in result and result["output"]:
                    output = result["output"]
                    if isinstance(output, list) and len(output) > 0:
                        image_url = output[0]
                    elif isinstance(output, str):
                        image_url = output
                
                # Download and save image locally
                local_path = ""
                if image_url:
                    local_path = self._download_image(image_url)
                
                # Save to history file
                if image_url:
                    self._save_to_history(image_url, prompt, local_path)
                
                if local_path:
                    return local_path
                elif image_url:
                    return image_url
                else:
                    return "Erro na resposta da API: URL da imagem não encontrada."
                    
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 429:
                    # Rate limit error - will retry
                    continue
                return f"Erro ao gerar imagem: {str(e)}"
            except requests.exceptions.RequestException as e:
                return f"Erro ao gerar imagem: {str(e)}"
            except Exception as e:
                return f"Erro ao gerar imagem: {str(e)}"
        
        # If we get here, all retries failed
        return "Erro: Não foi possível gerar a imagem após múltiplas tentativas. Tente novamente mais tarde."
    
    def _download_image(self, image_url: str) -> str:
        """
        Download image from URL to local images folder.
        
        Args:
            image_url: The image URL
            
        Returns:
            Local path to the downloaded image
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Generate filename from URL
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = ".webp"
            filename = f"image_{timestamp}{ext}"
            local_path = os.path.join(self.images_dir, filename)
            
            # Save image
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"DEBUG: Image downloaded to: {local_path}")
            return local_path
        except Exception as e:
            print(f"DEBUG: Failed to download image: {e}")
            return ""
    
    def _save_to_history(self, image_url: str, prompt: str, local_path: str = "") -> None:
        """
        Save image generation to history file.
        
        Args:
            image_url: The generated image URL
            prompt: The prompt used for generation
            local_path: Local path to the downloaded image
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{timestamp}] URL: {image_url}\nLocal: {local_path}\nPrompt: {prompt[:100]}...\n{'-' * 80}\n\n"
            
            # Append to history file
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(entry)
            
            print(f"DEBUG: Saved to history file: {self.history_file}")
        except Exception as e:
            print(f"DEBUG: Failed to save to history: {e}")
