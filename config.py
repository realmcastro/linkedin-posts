"""
Configuration module for NewsAPI Automation App.
Loads environment variables from .env file.
"""

import os
import sys
from dotenv import load_dotenv

# Determine the directory of the executable or script
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    application_path = os.path.dirname(sys.executable)
    print(f"[DEBUG] Running as executable from: {application_path}")
    
    # Try to find .env in multiple locations (in order of priority):
    # 1. PyInstaller temp folder (embedded .env)
    # 2. Same directory as executable (external .env)
    
    # PyInstaller temp folder path
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    env_paths = [
        os.path.join(bundle_dir, '.env'),  # Embedded in executable
        os.path.join(application_path, '.env'),  # External file next to exe
    ]
else:
    # Running as a normal Python script
    application_path = os.path.dirname(os.path.abspath(__file__))
    print(f"[DEBUG] Running as script from: {application_path}")
    env_paths = [os.path.join(application_path, '.env')]

# Try each .env path
env_loaded = False
for env_path in env_paths:
    print(f"[DEBUG] Looking for .env at: {env_path}")
    print(f"[DEBUG] .env exists: {os.path.exists(env_path)}")
    if os.path.exists(env_path):
        loaded = load_dotenv(env_path)
        print(f"[DEBUG] load_dotenv returned: {loaded}")
        if loaded:
            env_loaded = True
            print(f"[DEBUG] Loaded .env from: {env_path}")
            break

if not env_loaded:
    print(f"[DEBUG] WARNING: No .env file found in any location!")


class Config:
    """Configuration class for NewsAPI.org and ZAI settings."""
    
    # NewsAPI Configuration
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_BASE = os.getenv("NEWS_API_BASE", "https://newsapi.org/v2")
    
    # ZAI GLM API Configuration
    ZAI_API_KEY = os.getenv("ZAI_API_KEY")
    ZAI_API_BASE = os.getenv("ZAI_API_BASE", "https://api.z.ai/api/paas/v4")
    ZAI_MODEL = os.getenv("ZAI_MODEL", "glm-4.7")
    
    # Replicate API Configuration
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    
    # Request settings
    REQUEST_TIMEOUT = 120  # seconds
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY is not set in environment variables")
        return True
