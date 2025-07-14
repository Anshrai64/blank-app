# 🤖 AI ChatBot Pro

An advanced AI chatbot application with multimodal capabilities including live camera sharing, voice conversation, photo analysis, and real-time information retrieval.

## ✨ Features

### 💬 Advanced Chat
- Natural language conversations with AI
- Context-aware responses
- Real-time information with source links
- Smart conversation flow

### 📸 Camera Integration
- **Live Camera Sharing**: Real-time camera feed with AI analysis
- **Photo Upload**: Drag & drop image analysis
- **Visual Q&A**: Ask questions about what you see
- **Computer Vision**: Advanced image understanding

### 🎤 Voice Conversation
- **Speech-to-Text**: Natural voice input recognition
- **Text-to-Speech**: AI responses in voice format
- **Voice Settings**: Adjustable speed, pitch, and language
- **Multi-language Support**: English, Spanish, French, German

### 📚 Smart History
- **Conversation Logs**: Complete chat history tracking
- **Search & Filter**: Find specific conversations
- **Export Options**: JSON, TXT, CSV formats
- **Session Analytics**: Detailed usage statistics

### 🌐 Real-time Information
- **Live Data**: Up-to-date information retrieval
- **Source Citations**: Verified information sources
- **Fact Checking**: Confidence ratings for responses
- **Web Integration**: Real-time web search capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam (for camera features)
- Microphone (for voice features)
- Internet connection (for AI services)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-chatbot-pro
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (Optional)
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export GOOGLE_API_KEY="your-google-api-key"
   export GOOGLE_CSE_ID="your-custom-search-engine-id"
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start chatting with your AI assistant!

## 🛠️ Configuration

### API Keys Setup

For full functionality, configure these API keys in `config.py` or as environment variables:

- **OpenAI API Key**: For advanced AI responses and image analysis
- **Google API Key**: For real-time web search functionality
- **Custom Search Engine ID**: For Google search integration

### Camera Permissions

Grant camera permissions in your browser when prompted to enable:
- Live camera streaming
- Real-time visual analysis
- Photo capture features

### Microphone Permissions

Allow microphone access for:
- Voice message recording
- Speech-to-text conversion
- Voice conversation features

## 📱 Usage Guide

### Chat Interface
1. Type your message in the chat input
2. Click "🚀 Send Message" or press Enter
3. View AI responses with source citations
4. Use quick actions for camera and voice features

### Camera Features
1. Go to the "📸 Camera" tab
2. **Live Camera**: Enable camera for real-time analysis
3. **Photo Upload**: Drag & drop images for analysis
4. Ask questions about visual content

### Voice Conversation
1. Navigate to the "🎤 Voice" tab
2. Click the record button to start speaking
3. Process voice input for text conversion
4. Receive both text and audio responses

### Chat History
1. Access the "📚 History" tab
2. Filter conversations by type (Text, Voice, Camera)
3. Search specific content or topics
4. Export history in multiple formats

## 🏗️ Architecture

### Core Components

- **`streamlit_app.py`**: Main application interface
- **`ai_service.py`**: AI integration and response generation
- **`config.py`**: Configuration management
- **`utils.py`**: Utility functions and helpers

### Key Technologies

- **Frontend**: Streamlit with custom CSS
- **AI Processing**: OpenAI GPT-4 (with fallback simulation)
- **Voice**: SpeechRecognition + Google Text-to-Speech
- **Camera**: WebRTC real-time streaming
- **Image Processing**: PIL, OpenCV, Computer Vision
- **Real-time Data**: Web search integration

### Data Flow

1. **User Input** → Text, Voice, or Image
2. **Processing** → AI Service analyzes input
3. **AI Response** → Generated with sources
4. **Output** → Text, Voice, and Visual feedback
5. **Storage** → Session-based history tracking

## 🎨 UI Design

### Modern Interface
- Gradient color schemes
- Responsive design
- Clean typography
- Intuitive navigation

### Navigation Tabs
- **💬 Chat**: Main conversation interface
- **📸 Camera**: Live camera and photo upload
- **🎤 Voice**: Voice conversation settings
- **📚 History**: Chat history and analytics
- **ℹ️ Info**: App information and status

### Visual Elements
- Feature cards with gradients
- Real-time status indicators
- Performance metrics
- Session analytics

## 🔧 Customization

### Themes and Colors
Modify colors in `config.py`:
```python
PRIMARY_COLOR = "#667eea"
SECONDARY_COLOR = "#764ba2"
BACKGROUND_COLOR = "#f8f9fa"
```

### AI Model Configuration
Update AI settings:
```python
OPENAI_MODEL = "gpt-4-vision-preview"
MAX_CHAT_HISTORY = 100
SESSION_TIMEOUT = 3600
```

### Voice Settings
Customize voice features:
```python
SPEECH_RECOGNITION_LANGUAGE = "en-US"
TTS_LANGUAGE = "en"
TTS_SLOW = False
```

## 📊 Performance

### Optimization Features
- Async AI processing
- Image compression
- Session cleanup
- Rate limiting
- Caching mechanisms

### Monitoring
- Response time tracking
- Error handling
- Usage analytics
- Performance metrics

## 🔒 Security

### Data Privacy
- Session-based storage only
- No persistent data retention
- Local image processing
- Secure API communication

### Rate Limiting
- Request throttling
- User session limits
- API usage controls
- Resource management

## 🚀 Production Deployment

### Environment Setup
1. Set production environment variables
2. Configure secure API keys
3. Set up monitoring and logging
4. Implement database storage (optional)

### Scaling Considerations
- Use Redis for session storage
- Implement load balancing
- Add CDN for static assets
- Monitor resource usage

## 🐛 Troubleshooting

### Common Issues

**Camera not working:**
- Check browser permissions
- Ensure HTTPS connection
- Verify camera availability

**Voice features not responding:**
- Grant microphone permissions
- Check audio drivers
- Verify internet connection

**AI responses slow:**
- Check API key configuration
- Monitor rate limits
- Verify internet connectivity

### Debug Mode
Enable debug logging by setting:
```python
DEBUG = True
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 integration
- Streamlit for the web framework
- WebRTC for real-time communication
- Google for speech services
- Open source community

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review troubleshooting guide

---

**Built with ❤️ by AI Engineering Team**

*AI ChatBot Pro - The future of conversational AI*
