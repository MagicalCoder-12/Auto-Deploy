@echo off
echo Auto Deploy Agent CLI
echo ========================
echo.
echo This script will run the deploy agent which will:
echo 1. Detect your project type
echo 2. Recommend the best hosting platform
echo 3. Guide you through installation of required tools
echo 4. Deploy your site (or provide deployment instructions)
echo.
echo Press any key to continue...
pause >nul
echo.
echo Running Auto Deploy Agent...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Change to the script directory to ensure we can find our modules
cd /d "%SCRIPT_DIR%"

REM Add the script directory to PYTHONPATH so modules can be found
set PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%

REM Run the main.py file which contains the modularized code
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  An error occurred while running the deploy agent.
    echo Please make sure:
    echo 1. Python is installed and accessible from the command line
    echo 2. Required dependencies are installed (pip install -r requirements.txt)
    echo 3. Ollama is installed and the llama3.1:8b model is pulled
    echo.
    echo For more information, check the README.md file.
)

echo.
echo Deployment process completed.
echo Note: For some platforms (like GitHub Pages), you may need to
echo complete manual steps to finish deployment.
echo Press any key to exit...
pause >nul