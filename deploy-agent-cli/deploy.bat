@echo off
echo 🚀 Auto Deploy Agent CLI
echo ========================
echo.
echo This script will run the deploy agent which will:
echo 1. Detect your project type
echo 2. Recommend the best hosting platform
echo 3. Guide you through installation of required tools
echo 4. Deploy your site
echo.
echo Press any key to continue...
pause >nul
echo.
python deploy_agent.py
echo.
echo Deployment process completed.
echo Press any key to exit...
pause >nul