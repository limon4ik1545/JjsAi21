@echo off
REM JjsAi21 - AI Launcher
REM This script runs the trained AI to analyze gameplay videos

echo ============================================
echo    JjsAi21 - Analysis Mode
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

REM Check if model exists
if not exist "models\best_model.pth" (
    echo [ERROR] Trained model not found!
    echo Please run start_training.bat first to train the AI model.
    echo.
    pause
    exit /b 1
)

echo [INFO] Model found: models\best_model.pth
echo.

REM Get video file from user
set /p VIDEO_PATH="Enter path to video file for analysis (or press Enter for default): "

if "%VIDEO_PATH%"=="" (
    REM Check for sample video
    if exist "videos\sample_gameplay.mp4" (
        set VIDEO_PATH=videos\sample_gameplay.mp4
    ) else (
        echo [ERROR] No video path provided and no sample video found
        echo Please provide a video path or add a video to videos\
        pause
        exit /b 1
    )
)

REM Verify video file exists
if not exist "%VIDEO_PATH%" (
    echo [ERROR] Video file not found: %VIDEO_PATH%
    pause
    exit /b 1
)

echo.
echo [INFO] Analyzing video: %VIDEO_PATH%
echo.

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo ============================================
echo    Starting Video Analysis...
echo ============================================
echo.

REM Run analysis
python train.py --mode analyze --video "%VIDEO_PATH%" --model models\best_model.pth

if errorlevel 1 (
    echo.
    echo [ERROR] Analysis failed. Check logs/training.log for details
    pause
    exit /b 1
)

echo.
echo ============================================
echo    Analysis Completed Successfully!
echo ============================================
echo.
echo Results saved to: logs\analysis_results_*.json
echo.
echo Open the JSON file to see:
echo - Detected actions and skills
echo - Confidence scores
echo - Frame ranges for each detection
echo.

pause
