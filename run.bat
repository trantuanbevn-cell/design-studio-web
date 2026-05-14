@echo off
cls
echo ========================================
echo 🎨 Design Studio Web API
echo ========================================
echo.

REM Set environment variables
set GEMINI_API_KEY=AIzaSyAWy_LXeM7Jzve5WQ45WDHtbxssVptp7XI
set GOOGLE_CLOUD_PROJECT=682230388029
set PYTHONUNBUFFERED=1

echo ✓ Environment configured
echo ✓ Starting server...
echo.
echo ========================================
echo 🚀 Server running at:
echo    http://localhost:8000/static/index.html
echo ========================================
echo.
echo Press Ctrl+C to stop
echo.

python -m uvicorn backend.main:app --reload --port 8000 --host 0.0.0.0
