#!/bin/bash

# 🌐 Web Deployment Script for Deformed Grid Art Generator
# This script sets up and deploys the application for web browsers using pygbag

set -e  # Exit on any error

echo "🎨 Deformed Grid - Web Deployment Setup"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "🔄 Activating virtual environment..."
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ No virtual environment found. Please create one first:"
        echo "   python -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
        exit 1
    fi
fi

# Install pygbag if not already installed
echo "🔄 Checking pygbag installation..."
if ! python -c "import pygbag" 2>/dev/null; then
    echo "📦 Installing pygbag..."
    pip install pygbag --upgrade
    echo "✅ pygbag installed successfully"
else
    echo "✅ pygbag already installed"
fi

# Function to display deployment options
show_options() {
    echo ""
    echo "🚀 Deployment Options:"
    echo "1. Test locally (recommended first step)"
    echo "2. Build for production"
    echo "3. Build and run test server"
    echo "4. Build for itch.io deployment"
    echo "5. Show advanced options"
    echo "6. Exit"
    echo ""
}

# Function to run local test
test_locally() {
    echo "🧪 Testing locally (non-web mode)..."
    python main.py
}

# Function to build for production
build_production() {
    echo "🏗️ Building for production..."
    pygbag --build .
    echo ""
    echo "✅ Production build complete!"
    echo "📁 Files are ready in: build/web/"
    echo "🌐 Upload the contents of build/web/ to your web server"
}

# Function to build and run test server
build_and_run() {
    echo "🏗️ Building and starting test server..."
    echo "🌐 This will open your web browser automatically"
    echo "⏸️ Press Ctrl+C to stop the server when done"
    pygbag .
}

# Function to build for itch.io
build_itch() {
    echo "🎮 Building for itch.io..."
    pygbag --archive .
    echo ""
    echo "✅ itch.io build complete!"
    echo "📦 Upload build/web.zip to itch.io"
    echo "🎮 Set your itch.io project type to 'HTML' when uploading"
}

# Function to show advanced options
show_advanced() {
    echo ""
    echo "🔧 Advanced Options:"
    echo ""
    echo "Custom build commands:"
    echo "  pygbag --build .                    # Build only (no server)"
    echo "  pygbag --port 8080 .               # Custom port"
    echo "  pygbag --app_name 'My Art' .       # Custom app name"
    echo "  pygbag --archive .                 # Create itch.io zip"
    echo "  pygbag --html .                    # HTML embed version"
    echo ""
    echo "📚 For more options, see: README-WEB.md"
    echo "🌐 pygbag documentation: https://github.com/pygame-web/pygbag"
}

# Main menu loop
while true; do
    show_options
    read -p "Choose an option (1-6): " choice
    
    case $choice in
        1)
            test_locally
            ;;
        2)
            build_production
            ;;
        3)
            build_and_run
            ;;
        4)
            build_itch
            ;;
        5)
            show_advanced
            ;;
        6)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please choose 1-6."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done