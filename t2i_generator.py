"""
T2I Generator Module
Handles image generation using the Z.AI API.
"""

import requests
import time
from typing import Optional
from config import Config


class T2IGenerator:
    """Generator for images using Z.AI API."""
    
    def __init__(self):
        """Initialize T2I generator."""
        self.api_key = Config.ZAI_API_KEY
        self.api_base = Config.ZAI_API_BASE
        self.timeout = 120  # seconds - image generation can take longer
    
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
        Generate an image based on the LinkedIn post using Z.AI API.
        
        Args:
            post: The LinkedIn post text
            
        Returns:
            The image URL as a string
        """
        if not post:
            return "No post content available for image generation."
        
        # Extract theme from post
        theme = self._extract_theme_from_post(post)
        
        # Build the prompt for image generation
        prompt = f"""Conceptual professional LinkedIn image about: {theme}.
Minimalist, corporate, serious tone.
High contrast, dark background.
Symbolic representation of power, technology and impact.
No text, no logos, no people smiling."""
        
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
                url = f"{self.api_base}/images/generations"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "cogView-4-250304",
                    "prompt": prompt,
                    "size": "1024x1024",
                    "quality": "standard"
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
                
                # Extract the image URL from the response
                if "data" in result and len(result["data"]) > 0:
                    return result["data"][0].get("url", "")
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
