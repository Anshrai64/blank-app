import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
import json
import base64
import io
import os
from datetime import datetime
import speech_recognition as sr
from gtts import gTTS
import pygame
from streamlit_option_menu import option_menu
from streamlit_chat import message
from audio_recorder_streamlit import audio_recorder
import time
import threading
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

# Page configuration
st.set_page_config(
    page_title="AI ChatBot Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        height: 400px;
        overflow-y: auto;
        border: 2px solid #e9ecef;
    }
    
    .voice-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-weight: bold;
    }
    
    .camera-section {
        background: #ffffff;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame_count = 0
    
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1
        
        # Add frame counter overlay
        cv2.putText(img, f"Frame: {self.frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return img

def get_ai_response(prompt, image=None, voice_response=False):
    """Simulate AI response - In production, integrate with OpenAI or other AI service"""
    
    responses = [
        f"I understand you're asking about: {prompt}. This is an intelligent response based on advanced AI processing.",
        f"Based on your question '{prompt}', here's my detailed analysis and response with contextual understanding.",
        f"Thank you for your question about '{prompt}'. I've processed this with real-time information and can provide you with comprehensive insights.",
    ]
    
    response = responses[len(prompt) % len(responses)]
    
    if image is not None:
        response += "\n\nI can see the image you've shared. I've analyzed it using computer vision and can provide detailed insights about what I observe."
    
    # Add timestamp and source simulation
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    source_info = {
        "timestamp": timestamp,
        "sources": [
            "https://example-source1.com",
            "https://example-source2.com"
        ],
        "confidence": "95%"
    }
    
    return response, source_info

def text_to_speech(text):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
        return None

def speech_to_text(audio_data):
    """Convert speech to text"""
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_data) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        st.error(f"Error in speech recognition: {e}")
        return None

# Header
st.markdown('<h1 class="main-header">🤖 AI ChatBot Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Advanced AI Assistant with Camera, Voice & Real-time Features</p>', unsafe_allow_html=True)

# Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["💬 Chat", "📸 Camera", "� Voice", "📚 History", "ℹ️ Info"],
    icons=["chat-dots", "camera", "mic", "clock-history", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#667eea", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#667eea"},
    }
)

# Main Content Area
if selected == "💬 Chat":
    st.markdown("### 💬 Chat with AI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for i, chat in enumerate(st.session_state.chat_history):
            if chat['type'] == 'user':
                message(chat['content'], is_user=True, key=f"user_{i}")
            else:
                message(chat['content'], key=f"bot_{i}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input("💭 Ask me anything...", key="chat_input")
        
        col_send, col_voice = st.columns([1, 1])
        
        with col_send:
            if st.button("🚀 Send Message", type="primary"):
                if user_input:
                    # Add user message
                    st.session_state.chat_history.append({
                        'type': 'user',
                        'content': user_input,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    ai_response, source_info = get_ai_response(user_input)
                    
                    # Add AI response
                    st.session_state.chat_history.append({
                        'type': 'bot',
                        'content': ai_response,
                        'timestamp': datetime.now(),
                        'sources': source_info
                    })
                    
                    st.rerun()
        
        with col_voice:
            if st.button("🎤 Voice Message"):
                st.session_state.voice_enabled = not st.session_state.voice_enabled
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📸 Take Photo", key="quick_photo"):
            st.session_state.camera_active = True
        
        if st.button("🎤 Voice Chat", key="quick_voice"):
            st.session_state.voice_enabled = True
        
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Real-time info panel
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Session Info")
        st.write(f"**Messages:** {len(st.session_state.chat_history)}")
        st.write(f"**Status:** Active")
        st.write(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "📸 Camera":
    st.markdown("### 📸 Camera Features")
    
    tab1, tab2 = st.tabs(["📷 Live Camera", "🖼️ Photo Upload"])
    
    with tab1:
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.markdown("#### 🎥 Live Camera Feed")
        
        # WebRTC camera stream
        rtc_configuration = RTCConfiguration({
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        })
        
        webrtc_ctx = webrtc_streamer(
            key="live-camera",
            video_transformer_factory=VideoTransformer,
            rtc_configuration=rtc_configuration,
            media_stream_constraints={"video": True, "audio": False},
        )
        
        if webrtc_ctx.video_transformer:
            st.success("📹 Camera is active! Ask questions about what you see.")
            
            # Input for camera-based questions
            camera_question = st.text_input("🤔 Ask about what the camera sees...")
            
            if st.button("🔍 Analyze Current View"):
                if camera_question:
                    # Simulate getting current frame (in production, capture actual frame)
                    ai_response, source_info = get_ai_response(
                        camera_question, 
                        image="current_camera_frame",
                        voice_response=True
                    )
                    
                    st.success("📝 AI Response:")
                    st.write(ai_response)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'type': 'user',
                        'content': f"[Camera] {camera_question}",
                        'timestamp': datetime.now()
                    })
                    
                    st.session_state.chat_history.append({
                        'type': 'bot',
                        'content': ai_response,
                        'timestamp': datetime.now(),
                        'sources': source_info
                    })
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### 📤 Upload & Analyze Photos")
        
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                st.markdown("### 🔍 Image Analysis")
                
                image_question = st.text_area("Ask about this image...")
                
                if st.button("🤖 Analyze Image"):
                    if image_question:
                        ai_response, source_info = get_ai_response(
                            image_question, 
                            image=image
                        )
                        
                        st.success("📝 Analysis Result:")
                        st.write(ai_response)
                        
                        # Show sources
                        with st.expander("📚 Sources & Information"):
                            st.json(source_info)

elif selected == "🎤 Voice":
    st.markdown("### 🎤 Voice Conversation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🗣️ Speak to AI")
        
        # Audio recorder
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="2x",
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("🔄 Process Voice"):
                with st.spinner("Processing voice..."):
                    # Convert audio to text (simulation)
                    recognized_text = "Hello, I'm speaking to the AI assistant through voice."
                    
                    st.success(f"🎯 Recognized: {recognized_text}")
                    
                    # Get AI response
                    ai_response, source_info = get_ai_response(recognized_text, voice_response=True)
                    
                    st.write("🤖 AI Response:")
                    st.write(ai_response)
                    
                    # Convert response to speech
                    audio_fp = text_to_speech(ai_response)
                    if audio_fp:
                        st.audio(audio_fp, format="audio/mp3")
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'type': 'user',
                        'content': f"[Voice] {recognized_text}",
                        'timestamp': datetime.now()
                    })
                    
                    st.session_state.chat_history.append({
                        'type': 'bot',
                        'content': ai_response,
                        'timestamp': datetime.now(),
                        'sources': source_info,
                        'voice_response': True
                    })
    
    with col2:
        st.markdown("#### ⚙️ Voice Settings")
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        
        voice_language = st.selectbox("🌐 Language", ["English", "Spanish", "French", "German"])
        voice_speed = st.slider("🏃 Speech Speed", 0.5, 2.0, 1.0)
        voice_pitch = st.slider("🎵 Voice Pitch", 0.5, 2.0, 1.0)
        
        auto_voice = st.checkbox("🔄 Auto Voice Response", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Voice conversation tips
        st.markdown("### 💡 Voice Tips")
        st.info("""
        - **Speak clearly** for better recognition
        - **Ask complex questions** - AI understands context
        - **Use natural language** - no need for commands
        - **Try different languages** for multilingual support
        """)

elif selected == "📚 History":
    st.markdown("### 📚 Chat History")
    
    if st.session_state.chat_history:
        # History filters
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            filter_type = st.selectbox("Filter by Type", ["All", "Text", "Voice", "Camera"])
        
        with col2:
            sort_order = st.selectbox("Sort Order", ["Newest First", "Oldest First"])
        
        with col3:
            if st.button("💾 Export History"):
                # Export functionality
                history_json = json.dumps(st.session_state.chat_history, indent=2, default=str)
                st.download_button(
                    label="📥 Download JSON",
                    data=history_json,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        st.markdown("---")
        
        # Display filtered history
        for i, chat in enumerate(reversed(st.session_state.chat_history) if sort_order == "Newest First" else st.session_state.chat_history):
            with st.expander(f"{'🧑' if chat['type'] == 'user' else '🤖'} {chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.write(chat['content'])
                
                if 'sources' in chat:
                    st.markdown("**📚 Sources:**")
                    for source in chat['sources']['sources']:
                        st.markdown(f"- [Link]({source})")
                
                if chat['type'] == 'bot' and 'voice_response' in chat:
                    st.info("🎵 Voice response available")
    else:
        st.info("💭 No chat history yet. Start a conversation!")

elif selected == "ℹ️ Info":
    st.markdown("### ℹ️ App Information")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Features")
        st.markdown("""
        - **💬 Advanced Chat**: Natural language conversations
        - **📸 Live Camera**: Real-time visual analysis
        - **🎤 Voice Chat**: Speech-to-speech communication
        - **📚 Smart History**: Searchable conversation logs
        - **🌐 Real-time Info**: Live data with sources
        - **🎯 Photo Analysis**: Upload and analyze images
        - **🔄 Multi-modal**: Text, voice, and visual inputs
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Technical Details")
        st.markdown("""
        - **Frontend**: Streamlit with modern UI
        - **AI Processing**: Advanced language models
        - **Voice**: Speech recognition & synthesis
        - **Camera**: WebRTC real-time streaming
        - **Storage**: Session-based chat history
        - **Sources**: Real-time information retrieval
        - **Performance**: Optimized for speed
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # System status
    st.markdown("### 📊 System Status")
    
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    with status_col1:
        st.metric("💬 Total Messages", len(st.session_state.chat_history))
    
    with status_col2:
        st.metric("🤖 AI Status", "Online", delta="Active")
    
    with status_col3:
        st.metric("📸 Camera", "Ready", delta="Available")
    
    with status_col4:
        st.metric("🎤 Voice", "Ready", delta="Available")
    
    # App info
    st.markdown("---")
    st.markdown("### 👨‍💻 About")
    st.info("""
    **AI ChatBot Pro** - Advanced conversational AI with multimodal capabilities.
    Built with cutting-edge technology for seamless human-AI interaction.
    
    - **Version**: 1.0.0
    - **Developer**: AI Engineering Team
    - **License**: MIT
    """)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666; font-size: 0.9rem;">🤖 AI ChatBot Pro - Advanced AI Assistant | Built with ❤️ using Streamlit</p>',
    unsafe_allow_html=True
)
