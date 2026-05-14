@echo off
cls
echo ========================================
echo 🎨 Design Studio Web - Setup
echo ========================================
echo.
echo Step 1: Installing dependencies...
pip install -q fastapi uvicorn google-cloud-aiplatform python-dotenv sqlalchemy pillow python-multipart
echo ✓ Dependencies installed
echo.
echo Step 2: Creating project structure...
if not exist backend mkdir backend
if not exist backend\core mkdir backend\core
if not exist backend\api mkdir backend\api
if not exist frontend mkdir frontend
if not exist uploads mkdir uploads
if not exist renders mkdir renders
echo ✓ Folders created
echo.
echo ========================================
echo ✅ Setup complete!
echo ========================================
echo.
echo Next: Run "run.bat" to start server
pause
