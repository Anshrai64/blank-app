import openai
import requests
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import asyncio
import aiohttp
from config import Config

class AIService:
    """AI Service for handling OpenAI integration and real-time information"""
    
    def __init__(self):
        self.config = Config()
        # Initialize OpenAI client if API key is available
        if self.config.OPENAI_API_KEY and self.config.OPENAI_API_KEY != "your-openai-api-key-here":
            openai.api_key = self.config.OPENAI_API_KEY
            self.openai_available = True
        else:
            self.openai_available = False
    
    def encode_image(self, image: Image.Image) -> str:
        """Encode PIL Image to base64 string"""
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    
    async def get_ai_response(self, 
                            prompt: str, 
                            image: Optional[Image.Image] = None,
                            include_sources: bool = True,
                            conversation_history: List[Dict] = None) -> Tuple[str, Dict]:
        """Get AI response with optional image analysis and real-time information"""
        
        try:
            if self.openai_available:
                return await self._get_openai_response(prompt, image, include_sources, conversation_history)
            else:
                return await self._get_simulated_response(prompt, image, include_sources)
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            return error_response, self._create_source_info(error=str(e))
    
    async def _get_openai_response(self, 
                                 prompt: str, 
                                 image: Optional[Image.Image] = None,
                                 include_sources: bool = True,
                                 conversation_history: List[Dict] = None) -> Tuple[str, Dict]:
        """Get response from OpenAI API"""
        
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = "user" if msg['type'] == 'user' else "assistant"
                messages.append({"role": role, "content": msg['content']})
        
        # Prepare the current message
        if image:
            # Vision model request
            image_data = self.encode_image(image)
            message_content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_data}}
            ]
        else:
            message_content = prompt
        
        messages.append({"role": "user", "content": message_content})
        
        # Add system message for better responses
        system_message = {
            "role": "system", 
            "content": "You are an advanced AI assistant with capabilities for text, voice, and visual analysis. Provide detailed, helpful, and accurate responses. When analyzing images, describe what you see in detail."
        }
        messages.insert(0, system_message)
        
        # Make API call
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model=self.config.OPENAI_MODEL if image else "gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Get real-time information if requested
        sources = {}
        if include_sources:
            sources = await self._get_real_time_info(prompt)
        
        return ai_response, self._create_source_info(sources=sources.get('sources', []))
    
    async def _get_simulated_response(self, 
                                    prompt: str, 
                                    image: Optional[Image.Image] = None,
                                    include_sources: bool = True) -> Tuple[str, Dict]:
        """Generate simulated AI response for demo purposes"""
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        base_responses = [
            f"I understand you're asking about: '{prompt}'. Based on my advanced AI processing, here's a comprehensive response with detailed analysis and insights.",
            f"Thank you for your question: '{prompt}'. I've analyzed this using multiple AI models and can provide you with accurate, contextual information.",
            f"Regarding '{prompt}' - I've processed this query using natural language understanding and can offer detailed guidance and information.",
        ]
        
        response = base_responses[len(prompt) % len(base_responses)]
        
        if image:
            response += "\n\n🖼️ **Image Analysis**: I can see the image you've shared. Using computer vision analysis, I observe various elements including objects, colors, composition, and context. This visual information enhances my understanding of your query."
        
        # Add contextual information
        response += f"\n\n📊 **Context**: This response was generated at {datetime.now().strftime('%H:%M:%S')} with real-time processing capabilities."
        
        # Simulate sources
        sources = []
        if include_sources:
            sources = [
                "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "https://openai.com/research",
                "https://arxiv.org/list/cs.AI/recent"
            ]
        
        return response, self._create_source_info(sources=sources)
    
    async def _get_real_time_info(self, query: str) -> Dict:
        """Fetch real-time information from web sources"""
        
        try:
            # Simulate web search (in production, use Google Custom Search API)
            search_results = {
                "sources": [
                    f"https://example-source-1.com/search?q={query.replace(' ', '+')}",
                    f"https://example-source-2.com/info/{query.replace(' ', '-')}",
                    f"https://example-source-3.com/data/{query.replace(' ', '_')}"
                ],
                "timestamp": datetime.now().isoformat(),
                "query": query
            }
            
            return search_results
            
        except Exception as e:
            return {"error": str(e), "sources": []}
    
    def _create_source_info(self, sources: List[str] = None, error: str = None) -> Dict:
        """Create source information dictionary"""
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": sources or [],
            "confidence": "95%" if not error else "N/A",
            "error": error,
            "real_time": True
        }
    
    async def analyze_image(self, image: Image.Image, question: str = None) -> Tuple[str, Dict]:
        """Analyze an image with optional specific question"""
        
        if not question:
            question = "Please analyze this image and describe what you see in detail."
        
        return await self.get_ai_response(question, image=image, include_sources=False)
    
    async def process_voice_query(self, text: str, conversation_history: List[Dict] = None) -> Tuple[str, Dict]:
        """Process voice query with conversation context"""
        
        voice_prompt = f"[Voice Query] {text}"
        return await self.get_ai_response(voice_prompt, conversation_history=conversation_history)
    
    def get_system_status(self) -> Dict:
        """Get system status information"""
        
        return {
            "openai_available": self.openai_available,
            "model": self.config.OPENAI_MODEL,
            "timestamp": datetime.now().isoformat(),
            "status": "online" if self.openai_available else "demo_mode"
        }

# Global AI service instance
ai_service = AIService()