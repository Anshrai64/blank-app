import os
from typing import Dict, Any

class Config:
    """Configuration class for AI ChatBot Pro"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-vision-preview")
    
    # Google Search Configuration  
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your-google-api-key-here")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "your-custom-search-engine-id")
    
    # Speech Configuration
    SPEECH_RECOGNITION_TIMEOUT = 5
    SPEECH_RECOGNITION_LANGUAGE = "en-US"
    TTS_LANGUAGE = "en"
    TTS_SLOW = False
    
    # Camera Configuration
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    CAMERA_FPS = 30
    
    # App Configuration
    APP_TITLE = "AI ChatBot Pro"
    APP_ICON = "🤖"
    MAX_CHAT_HISTORY = 100
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # UI Configuration
    PRIMARY_COLOR = "#667eea"
    SECONDARY_COLOR = "#764ba2"
    BACKGROUND_COLOR = "#f8f9fa"
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ["png", "jpg", "jpeg", "gif", "bmp", "webp"]
    
    # WebRTC Configuration
    RTC_CONFIGURATION = {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["stun:stun1.l.google.com:19302"]}
        ]
    }
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI configuration"""
        return {
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.OPENAI_MODEL
        }
    
    @classmethod
    def get_speech_config(cls) -> Dict[str, Any]:
        """Get speech recognition configuration"""
        return {
            "timeout": cls.SPEECH_RECOGNITION_TIMEOUT,
            "language": cls.SPEECH_RECOGNITION_LANGUAGE,
            "tts_language": cls.TTS_LANGUAGE,
            "tts_slow": cls.TTS_SLOW
        }
    
    @classmethod
    def get_camera_config(cls) -> Dict[str, Any]:
        """Get camera configuration"""
        return {
            "width": cls.CAMERA_WIDTH,
            "height": cls.CAMERA_HEIGHT,
            "fps": cls.CAMERA_FPS
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        required_settings = [
            cls.OPENAI_API_KEY,
            cls.APP_TITLE,
            cls.PRIMARY_COLOR
        ]
        
        return all(setting and setting != "your-openai-api-key-here" for setting in required_settings)