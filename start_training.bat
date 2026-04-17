@echo off
REM JjsAi21 - Training Launcher
REM This script starts the AI training process for Jujutsu Shenanigans gameplay analysis

echo ============================================
echo    JjsAi21 - Training Mode
echo    AI Video Analysis for Jujutsu Shenanigans
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Check if required packages are installed
echo [INFO] Checking dependencies...
python -c "import torch" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PyTorch not found. Installing dependencies...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
)

python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] OpenCV not found. Installing dependencies...
    pip install opencv-python
)

python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] NumPy not found. Installing dependencies...
    pip install numpy
)

echo.
echo [INFO] All dependencies checked
echo.

REM Create necessary directories
if not exist "data\videos" mkdir data\videos
if not exist "data\labels" mkdir data\labels
if not exist "models" mkdir models
if not exist "logs" mkdir logs

echo [INFO] Directories ready
echo.

REM Check for training data
if not exist "data\videos\*.mp4" (
    if not exist "data\videos\*.avi" (
        echo [WARNING] No training videos found in data\videos directory
        echo.
        echo Please add gameplay videos to: data\videos
        echo And corresponding label files to: data\labels
        echo.
        echo Example label format (JSON):
        echo {
        echo   "action": 0,
        echo   "timestamp": 123,
        echo   "description": "player_movement"
        echo }
        echo.
    )
)

echo ============================================
echo    Starting Training Process...
echo ============================================
echo.

REM Run training
python train.py --mode train --config config/training_config.json

if errorlevel 1 (
    echo.
    echo [ERROR] Training failed. Check logs/training.log for details
    pause
    exit /b 1
)

echo.
echo ============================================
echo    Training Completed Successfully!
echo ============================================
echo.
echo Model saved to: models/best_model.pth
echo Logs available at: logs/training.log
echo.

pause
