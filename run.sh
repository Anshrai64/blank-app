#!/bin/bash

echo "🤖 Starting AI ChatBot Pro..."

# Activate virtual environment
source venv/bin/activate

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing requirements..."
    pip install -r requirements.txt
fi

# Start the application
echo "🚀 Launching AI ChatBot Pro on http://localhost:8501"
echo "📝 Note: Some advanced features require API keys (see .env.example)"
echo "🎯 Press Ctrl+C to stop the application"

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0