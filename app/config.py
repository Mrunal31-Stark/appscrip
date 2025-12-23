import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Market Analysis API"
    VERSION: str = "1.0.0"
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "")
    
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY not found in .env file. AI analysis will fail.")

settings = Settings()
