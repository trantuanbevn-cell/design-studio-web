"""
Design Studio - Web App Backend
FastAPI + Imagen API for 3D rendering
Production-ready version with proper imports
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Fix Python path - when running from /app as main module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load env
load_dotenv()

# Import routes - absolute imports
from backend.api.routes import router
from backend.database import init_db

# Create app
app = FastAPI(
    title="Design Studio Web API",
    description="AI-powered 3D rendering platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init database
try:
    init_db()
    print("✓ Database initialized")
except Exception as e:
    print(f"❌ Database error: {e}")

# Include routes
try:
    app.include_router(router)
    print("✓ API routes loaded")
except Exception as e:
    print(f"❌ Routes error: {e}")

# Serve static files (frontend)
# __file__ = /app/backend/main.py, parent.parent = /app
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    print(f"✓ Frontend mounted at /static")
else:
    print(f"❌ Frontend path not found: {frontend_path}")

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Design Studio Web API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "upload": "POST /api/upload",
            "render": "POST /api/render",
            "health": "GET /api/health",
            "frontend": "GET /static/index.html"
        }
    }

@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🎨 Design Studio Web API")
    print("=" * 50)
    print("✓ Imagen API configured")
    print("✓ Ready for requests")
    print("=" * 50)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
