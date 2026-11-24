@echo off
echo === Local Debugging Agent Setup (Windows) ===

REM Check if ollama is installed
where ollama >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Ollama not found.
    echo Please download and install Ollama from: https://ollama.com/download/windows
    echo After installing, re-run this script.
    pause
    exit /b 1
) ELSE (
    echo Ollama already installed.
)

REM Pull the model
echo Pulling qwen2.5-coder:7b model (~4GB, one-time download)...
ollama pull qwen2.5-coder:7b

REM Install Python dependencies
echo Installing Python dependencies...
pip install ollama rich

echo.
echo === Setup Complete ===
echo Run the agent with: python agent.py
pause
