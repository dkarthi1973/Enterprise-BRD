#!/bin/bash

# Enterprise BRD Template Generator - Startup Script

echo "=========================================="
echo "Enterprise BRD Template Generator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt -q
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "Starting Streamlit application..."
echo "The application will open at: http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

# Run Streamlit
streamlit run app.py --logger.level=info
