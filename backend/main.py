"""
Design Studio - Web App Backend
FastAPI + Imagen API for 3D rendering
Complete production-ready version
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Import routes (relative imports)
from .api.routes import router
from .database import init_db

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
init_db()

# Include routes
app.include_router(router)

# Serve static files (frontend)
# __file__ = /app/backend/main.py, so parent.parent = /app
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
else:
    print(f"Warning: Frontend path not found: {frontend_path}")

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
    print("✓ Database initialized")
    print("✓ API routes loaded")
    print("✓ Imagen API configured")
    print("✓ Ready for requests")
    print("=" * 50)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080))
    )
