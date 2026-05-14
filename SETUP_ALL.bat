@echo off
cls
color 0A
echo.
echo ========================================
echo 🎨 Design Studio Web - Complete Setup
echo ========================================
echo.

REM Step 1: Create folders
echo [1/4] Creating folders...
if not exist backend mkdir backend
if not exist backend\core mkdir backend\core
if not exist backend\api mkdir backend\api
if not exist frontend mkdir frontend
if not exist uploads mkdir uploads
if not exist renders mkdir renders
echo ✓ Folders created
echo.

REM Step 2: Create Python files
echo [2/4] Creating Python files...
call create_files.bat
call create_routes.bat
call create_frontend.bat
echo.

REM Step 3: Install dependencies
echo [3/4] Installing dependencies...
echo Please wait...
pip install -q fastapi uvicorn google-cloud-aiplatform python-dotenv sqlalchemy pillow python-multipart
echo ✓ Dependencies installed
echo.

REM Step 4: Ready to run
echo [4/4] Setup complete!
echo.
echo ========================================
echo ✅ All Done!
echo ========================================
echo.
echo 🚀 To start the server, double-click:
echo    → run.bat
echo.
echo 📱 Then open browser:
echo    → http://localhost:8000/static/index.html
echo.
pause
