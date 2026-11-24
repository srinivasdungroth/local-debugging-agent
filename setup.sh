#!/bin/bash
set -e

echo "=== Local Debugging Agent Setup ==="

# Detect OS
OS="$(uname -s)"
echo "Detected OS: $OS"

# Check ollama installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    if [ "$OS" = "Darwin" ] || [ "$OS" = "Linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "Windows detected: Please install Ollama manually from https://ollama.com/download"
        echo "Then re-run this script in Git Bash or WSL."
        exit 1
    fi
else
    echo "Ollama already installed: $(ollama --version)"
fi

# Start ollama server if not already running
if ! pgrep -x "ollama" > /dev/null 2>&1; then
    echo "Starting Ollama server..."
    if [ "$OS" = "Darwin" ] || [ "$OS" = "Linux" ]; then
        ollama serve > /tmp/ollama.log 2>&1 &
    fi
    sleep 3
else
    echo "Ollama server already running."
fi

# Pull the model
echo "Pulling qwen2.5-coder:7b model (~4GB, one-time download)..."
ollama pull qwen2.5-coder:7b

# Install Python dependencies
echo "Installing Python dependencies..."
pip install ollama rich

echo ""
echo "=== Setup Complete ==="
echo "Run the agent with: python3 agent.py"
