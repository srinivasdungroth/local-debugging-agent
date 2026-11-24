#!/bin/bash
set -e

echo "=== Local Debugging Agent Setup ==="

# Check ollama installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama already installed: $(ollama --version)"
fi

# Start ollama in background if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama server..."
    ollama serve &>/tmp/ollama.log &
    sleep 3
fi

# Pull model (llama3.2 ~2GB - fast and good for code)
echo "Pulling llama3.2 model (~2GB, one-time download)..."
ollama pull llama3.2

echo ""
echo "=== Setup Complete ==="
echo "Run the agent with: python3 agent.py"
