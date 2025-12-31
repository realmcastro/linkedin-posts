"""
ZAI Classifier Module
Handles classification of news articles using ZAI GLM API.
"""

import requests
import time
from typing import List, Dict
from config import Config
from zai_prompts import ZAIPrompts


class ZAIClassifier:
    """Classifier for news articles using ZAI GLM API."""
    
    def __init__(self):
        """Initialize<arg_key> ZAI classifier."""
        self.api_key = Config.ZAI_API_KEY
        self.api_base = Config.ZAI_API_BASE
        self.model = Config.ZAI_MODEL
        self.timeout = Config.REQUEST_TIMEOUT
    
    def classify_news(self, articles: List[Dict]) -> str:
        """
        Classify news articles using ZAI GLM API.
        
        Args:
            articles: List of article dictionaries with title, description, source, and publishedAt
            
        Returns:
            Classification result as a string
        """
        if not articles:
            return "Nenhuma notícia para classificar."
        
        # Build the news data string
        news_data = ""
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'N/A')
            description = article.get('description', 'N/A')
            source = article.get('source', {}).get('name', 'N/A')
            published_at = article.get('publishedAt', 'N/A')
            
            news_data += f"\nNotícia {i}\n"
            news_data += f"Título: {title}\n"
            news_data += f"Descrição: {description}\n"
            news_data += f"Fonte: {source}\n"
            news_data += f"Data: {published_at}\n"
        
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
                url = f"{self.api_base}/chat/completions"
                headers = {
                    "Accept-Language": "en-US,en",
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": ZAIPrompts.CLASSIFY_NEWS
                        },
                        {
                            "role": "user",
                            "content": news_data
                        }
                    ],
                    "temperature": 1,
                    "stream": False,
                    "do_sample": True,
                    "thinking": {
                        "type": "enabled",
                        "clear_thinking": True
                    },
                    "top_p": 0.95,
                    "tool_stream": False,
                    "response_format": {"type": "text"}
                }
                
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Check for rate limit error
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        # Will retry in next iteration with exponential backoff
                        continue
                    else:
                        return "Erro: Limite de taxa da API excedido. Tente novamente em alguns minutos."
                
                response.raise_for_status()
                result = response.json()
                
                # Extract the classification result
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "Erro na resposta da API: formato inesperado."
                    
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 429:
                    # Rate limit error - will retry
                    continue
                return f"Erro ao classificar notícias: {str(e)}"
            except requests.exceptions.RequestException as e:
                return f"Erro ao classificar notícias: {str(e)}"
        
        # If we get here, all retries failed
        return "Erro: Não foi possível classificar após múltiplas tentativas. Tente novamente mais tarde."
    
    def generate_linkedin_post(self, classification_text: str) -> str:
        """
        Generate a LinkedIn post based on the classification result.
        
        Args:
            classification_text: The classification result from classify_news()
            
        Returns:
            Generated LinkedIn post as a string
        """
        if not classification_text:
            return "Nenhuma classificação disponível para gerar post."
        
        # Build the prompt with classification text
        user_content = ZAIPrompts.GENERATE_LINKEDIN_POST + "\n\n" + classification_text
        
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
                url = f"{self.api_base}/chat/completions"
                headers = {
                    "Accept-Language": "en-US,en",
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um assistente útil que gera posts de LinkedIn."
                        },
                        {
                            "role": "user",
                            "content": user_content
                        }
                    ],
                    "temperature": 1,
                    "stream": False,
                    "do_sample": True,
                    "thinking": {
                        "type": "enabled",
                        "clear_thinking": True
                    },
                    "top_p": 0.95,
                    "tool_stream": False,
                    "response_format": {"type": "text"}
                }
                
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Check for rate limit error
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        # Will retry in next iteration with exponential backoff
                        continue
                    else:
                        return "Erro: Limite de taxa da API excedido. Tente novamente em alguns minutos."
                
                response.raise_for_status()
                result = response.json()
                
                # Extract the LinkedIn post
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "Erro na resposta da API: formato inesperado."
                    
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 429:
                    # Rate limit error - will retry
                    continue
                return f"Erro ao gerar post: {str(e)}"
            except requests.exceptions.RequestException as e:
                return f"Erro ao gerar post: {str(e)}"
        
        # If we get here, all retries failed
        return "Erro: Não foi possível gerar o post após múltiplas tentativas. Tente novamente mais tarde."
