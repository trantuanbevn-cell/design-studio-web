@echo off
(
echo from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
echo from fastapi.responses import FileResponse
echo from sqlalchemy.orm import Session
echo from pathlib import Path
echo from datetime import datetime
echo from database import SessionLocal, Render
echo from core.dae_parser import DAEParser
echo from core.imagen_renderer import ImagenRenderer
echo.
echo router = APIRouter(prefix="/api", tags=["render"^^]^)
echo UPLOAD_DIR = Path("uploads"^)
echo UPLOAD_DIR.mkdir(exist_ok=True^)
echo.
echo def get_db(^):
echo     db = SessionLocal(^)
echo     try:
echo         yield db
echo     finally:
echo         db.close(^)
echo.
echo @router.post("/upload"^)
echo async def upload_file(file: UploadFile = File(...^), db: Session = Depends(get_db^)^):
echo     try:
echo         allowed = ['.dae', '.glb', '.obj'^]
echo         file_ext = Path(file.filename^).suffix.lower(^)
echo         if file_ext not in allowed:
echo             raise HTTPException(status_code=400, detail="File type not supported"^)
echo         file_path = UPLOAD_DIR / file.filename
echo         content = await file.read(^)
echo         if len(content^) ^> 500 * 1024 * 1024:
echo             raise HTTPException(status_code=413, detail="File too large"^)
echo         with open(file_path, "wb"^) as f:
echo             f.write(content^)
echo         parser = DAEParser(str(file_path^)^)
echo         if not parser.parse(^):
echo             raise HTTPException(status_code=400, detail="Failed to parse"^)
echo         scene_info = parser.get_info(^)
echo         return {"status": "success", "filename": file.filename, "size": len(content^), "scene": scene_info}
echo     except HTTPException:
echo         raise
echo     except Exception as e:
echo         raise HTTPException(status_code=500, detail=str(e^)^)
echo.
echo @router.post("/render"^)
echo async def render(filename: str = Form(...^), lighting: str = Form("interior_daylight"^), style: str = Form("Photorealistic"^), resolution: str = Form("2K"^), description: str = Form(""^), db: Session = Depends(get_db^)^):
echo     try:
echo         file_path = UPLOAD_DIR / filename
echo         if not file_path.exists(^):
echo             raise HTTPException(status_code=404, detail="File not found"^)
echo         parser = DAEParser(str(file_path^)^)
echo         if not parser.parse(^):
echo             raise HTTPException(status_code=400, detail="Failed to parse"^)
echo         scene_data = parser.get_data(^)
echo         options = {"lighting": lighting, "style": style, "resolution": resolution, "description": description, "space_type": "Interior"}
echo         renderer = ImagenRenderer(^)
echo         result = renderer.render(scene_data, options^)
echo         if not result:
echo             raise HTTPException(status_code=500, detail="Render failed"^)
echo         image_bytes, output_path = result
echo         return FileResponse(output_path, media_type="image/png", filename=f"render.png"^)
echo     except HTTPException:
echo         raise
echo     except Exception as e:
echo         raise HTTPException(status_code=500, detail=str(e^)^)
echo.
echo @router.get("/health"^)
echo async def health(^):
echo     return {"status": "ok", "service": "Design Studio Web API"}
echo.
echo @router.get("/status"^)
echo async def status(^):
echo     return {"api": "Design Studio Web", "supported_formats": [".dae", ".glb", ".obj"^^]}
) > backend\api\routes.py
echo ✓ routes.py created
