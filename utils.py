import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import hashlib
import os

class ChatUtils:
    """Utility functions for chat management"""
    
    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """Format timestamp for display"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    @staticmethod
    def export_chat_history(chat_history: List[Dict], format_type: str = "json") -> str:
        """Export chat history in various formats"""
        
        if format_type == "json":
            return json.dumps(chat_history, indent=2, default=str)
        
        elif format_type == "txt":
            lines = []
            for chat in chat_history:
                timestamp = chat['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                role = "User" if chat['type'] == 'user' else "AI"
                lines.append(f"[{timestamp}] {role}: {chat['content']}\n")
            return "\n".join(lines)
        
        elif format_type == "csv":
            import csv
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Timestamp", "Type", "Content", "Sources"])
            
            for chat in chat_history:
                sources = chat.get('sources', {}).get('sources', [])
                sources_str = "; ".join(sources) if sources else ""
                writer.writerow([
                    chat['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                    chat['type'],
                    chat['content'],
                    sources_str
                ])
            return output.getvalue()
        
        return ""
    
    @staticmethod
    def filter_chat_history(chat_history: List[Dict], filter_type: str = "all") -> List[Dict]:
        """Filter chat history by type"""
        
        if filter_type == "all":
            return chat_history
        elif filter_type == "text":
            return [chat for chat in chat_history if not chat['content'].startswith('[')]
        elif filter_type == "voice":
            return [chat for chat in chat_history if chat['content'].startswith('[Voice]')]
        elif filter_type == "camera":
            return [chat for chat in chat_history if chat['content'].startswith('[Camera]')]
        
        return chat_history
    
    @staticmethod
    def search_chat_history(chat_history: List[Dict], query: str) -> List[Dict]:
        """Search chat history for specific content"""
        
        query_lower = query.lower()
        return [
            chat for chat in chat_history
            if query_lower in chat['content'].lower()
        ]

class ImageUtils:
    """Utility functions for image processing"""
    
    @staticmethod
    def resize_image(image: Image.Image, max_size: Tuple[int, int] = (800, 600)) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    @staticmethod
    def base64_to_image(base64_str: str) -> Image.Image:
        """Convert base64 string to PIL Image"""
        
        img_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(img_data))
    
    @staticmethod
    def validate_image(uploaded_file) -> bool:
        """Validate uploaded image file"""
        
        if uploaded_file is None:
            return False
        
        try:
            image = Image.open(uploaded_file)
            # Check file size (10MB max)
            if uploaded_file.size > 10 * 1024 * 1024:
                return False
            return True
        except Exception:
            return False
    
    @staticmethod
    def add_image_watermark(image: Image.Image, text: str = "AI ChatBot Pro") -> Image.Image:
        """Add watermark to image"""
        
        from PIL import ImageDraw, ImageFont
        
        watermarked = image.copy()
        draw = ImageDraw.Draw(watermarked)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Position watermark at bottom right
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        margin = 10
        x = image.width - text_width - margin
        y = image.height - text_height - margin
        
        # Add semi-transparent background
        draw.rectangle([x-5, y-5, x+text_width+5, y+text_height+5], fill=(0, 0, 0, 128))
        draw.text((x, y), text, fill=(255, 255, 255, 180), font=font)
        
        return watermarked

class SessionUtils:
    """Utility functions for session management"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        
        defaults = {
            'chat_history': [],
            'voice_enabled': False,
            'camera_active': False,
            'user_preferences': {
                'theme': 'light',
                'voice_speed': 1.0,
                'auto_voice': True,
                'notifications': True
            },
            'session_start': datetime.now(),
            'message_count': 0
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def get_session_stats() -> Dict[str, Any]:
        """Get session statistics"""
        
        if 'chat_history' not in st.session_state:
            return {}
        
        chat_history = st.session_state.chat_history
        session_start = st.session_state.get('session_start', datetime.now())
        
        user_messages = [msg for msg in chat_history if msg['type'] == 'user']
        ai_messages = [msg for msg in chat_history if msg['type'] == 'bot']
        
        voice_messages = [msg for msg in chat_history if '[Voice]' in msg['content']]
        camera_messages = [msg for msg in chat_history if '[Camera]' in msg['content']]
        
        session_duration = datetime.now() - session_start
        
        return {
            'total_messages': len(chat_history),
            'user_messages': len(user_messages),
            'ai_messages': len(ai_messages),
            'voice_messages': len(voice_messages),
            'camera_messages': len(camera_messages),
            'session_duration': session_duration,
            'session_start': session_start,
            'avg_response_time': '< 2 seconds'  # Simulated
        }
    
    @staticmethod
    def cleanup_old_sessions():
        """Clean up old session data"""
        
        if 'chat_history' in st.session_state:
            # Keep only last 100 messages
            max_messages = 100
            if len(st.session_state.chat_history) > max_messages:
                st.session_state.chat_history = st.session_state.chat_history[-max_messages:]

class ValidationUtils:
    """Utility functions for validation"""
    
    @staticmethod
    def validate_text_input(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
        """Validate text input"""
        
        if not text or not text.strip():
            return False
        
        if len(text) < min_length or len(text) > max_length:
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        
        import re
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove extra spaces and dots
        filename = re.sub(r'\.+', '.', filename)
        filename = re.sub(r'\s+', '_', filename)
        
        return filename
    
    @staticmethod
    def check_rate_limit(user_id: str = "default", max_requests: int = 100, window_minutes: int = 60) -> bool:
        """Simple rate limiting check"""
        
        # In production, use Redis or database for persistence
        if 'rate_limits' not in st.session_state:
            st.session_state.rate_limits = {}
        
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        if user_id not in st.session_state.rate_limits:
            st.session_state.rate_limits[user_id] = []
        
        # Clean old requests
        st.session_state.rate_limits[user_id] = [
            req_time for req_time in st.session_state.rate_limits[user_id]
            if req_time > window_start
        ]
        
        # Check limit
        if len(st.session_state.rate_limits[user_id]) >= max_requests:
            return False
        
        # Add current request
        st.session_state.rate_limits[user_id].append(now)
        return True

class PerformanceUtils:
    """Utility functions for performance monitoring"""
    
    @staticmethod
    def measure_response_time(func):
        """Decorator to measure function response time"""
        
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            
            # Store in session state for analytics
            if 'performance_metrics' not in st.session_state:
                st.session_state.performance_metrics = []
            
            st.session_state.performance_metrics.append({
                'function': func.__name__,
                'response_time': response_time,
                'timestamp': start_time
            })
            
            return result
        return wrapper
    
    @staticmethod
    def get_performance_stats() -> Dict[str, Any]:
        """Get performance statistics"""
        
        if 'performance_metrics' not in st.session_state:
            return {}
        
        metrics = st.session_state.performance_metrics
        
        if not metrics:
            return {}
        
        response_times = [m['response_time'] for m in metrics]
        
        return {
            'total_requests': len(metrics),
            'avg_response_time': sum(response_times) / len(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'last_hour_requests': len([
                m for m in metrics
                if m['timestamp'] > datetime.now() - timedelta(hours=1)
            ])
        }