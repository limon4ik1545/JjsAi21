@echo off
echo ========================================
echo JjsAi21 Project Setup & Update Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo Python found.
echo.

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip. Continuing anyway...
)
echo.

echo [3/4] Installing/Updating required libraries...
pip install --upgrade -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements.
    pause
    exit /b 1
)
echo.

echo [4/4] Verifying installation...
python -c "import torch, torchvision, cv2, numpy; print('All libraries imported successfully!')"
if %errorlevel% neq 0 (
    echo WARNING: Some libraries might not be installed correctly.
    echo Please check the error messages above.
)
echo.

echo ========================================
echo Setup/Update completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Place your training videos in the 'videos' folder.
echo 2. Run 'start_training.bat' to start training the AI.
echo 3. Run 'start_ai.bat' to analyze new gameplay footage.
echo.
pause
