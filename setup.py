#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

print("=" * 50)
print("🎨 Design Studio Web - Setup")
print("=" * 50)

# Create folders
print("\n[1/3] Creating folders...")
folders = ["backend", "backend\\core", "backend\\api", "frontend", "uploads", "renders"]
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)
print("✓ Folders created")

# Create main.py
print("\n[2/3] Creating Python files...")
main_py = """from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
from api.routes import router
from database import init_db

app = FastAPI(title="Design Studio Web API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

init_db()
app.include_router(router)

@app.get("/")
async def root():
    return {"service": "Design Studio Web API", "status": "running"}

@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🎨 Design Studio Web API")
    print("=" * 50)
    print("✓ Ready for requests")
    print("=" * 50)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

database_py = """from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./design_studio.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)

class Render(Base):
    __tablename__ = "renders"
    id = Column(Integer, primary_key=True, index=True)

Session = SessionLocal

def init_db():
    Base.metadata.create_all(bind=engine)
"""

routes_py = """from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from database import SessionLocal
from core.dae_parser import DAEParser
from core.imagen_renderer import ImagenRenderer

router = APIRouter(prefix="/api", tags=["render"])
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        allowed = ['.dae', '.glb', '.obj']
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed:
            raise HTTPException(status_code=400, detail="File type not supported")
        file_path = UPLOAD_DIR / file.filename
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        parser = DAEParser(str(file_path))
        if not parser.parse():
            raise HTTPException(status_code=400, detail="Failed to parse")
        return {"status": "success", "filename": file.filename, "size": len(content), "scene": parser.get_info()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/render")
async def render(filename: str = Form(...), lighting: str = Form("interior_daylight"), style: str = Form("Photorealistic"), resolution: str = Form("2K"), description: str = Form(""), db: Session = Depends(get_db)):
    try:
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        parser = DAEParser(str(file_path))
        if not parser.parse():
            raise HTTPException(status_code=400, detail="Failed to parse")
        scene_data = parser.get_data()
        options = {"lighting": lighting, "style": style, "resolution": resolution, "description": description, "space_type": "Interior"}
        renderer = ImagenRenderer()
        result = renderer.render(scene_data, options)
        if not result:
            raise HTTPException(status_code=500, detail="Render failed")
        image_bytes, output_path = result
        return FileResponse(output_path, media_type="image/png", filename="render.png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok", "service": "Design Studio Web API"}
"""

dae_parser_py = """import xml.etree.ElementTree as ET
from pathlib import Path

class DAEParser:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = {"cameras": [], "meshes": [], "materials": [], "lights": [], "metadata": {"filename": self.filepath.name}}
    
    def parse(self):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            ns = {'dae': 'http://www.collada.org/2005/11/COLLADASchema'}
            for camera in root.findall('.//dae:camera', ns):
                self.data['cameras'].append({'name': camera.get('id', 'Camera')})
            for geometry in root.findall('.//dae:geometry', ns):
                self.data['meshes'].append({'name': geometry.get('id', 'Mesh')})
            for material in root.findall('.//dae:material', ns):
                self.data['materials'].append({'name': material.get('id', 'Material')})
            return len(self.data['meshes']) > 0
        except:
            return False
    
    def get_data(self):
        return self.data
    
    def get_info(self):
        return {"cameras": len(self.data['cameras']), "meshes": len(self.data['meshes']), "materials": len(self.data['materials'])}
"""

imagen_py = """import os
from pathlib import Path
import time

class ImagenRenderer:
    def __init__(self):
        self.project_id = "682230388029"
        self.location = "us-central1"
    
    def render(self, scene_data, options):
        try:
            prompt = self._build_prompt(scene_data, options)
            image_bytes = self._generate_image(prompt)
            if not image_bytes:
                return None
            output_path = self._save_image(image_bytes)
            return image_bytes, output_path
        except:
            return None
    
    def _build_prompt(self, scene_data, options):
        return f"Professional design, {options.get('style', 'Photorealistic')}, 4K"
    
    def _generate_image(self, prompt):
        try:
            from vertexai.vision_models import ImageGenerationModel
            import vertexai
            vertexai.init(project=self.project_id, location=self.location)
            model = ImageGenerationModel.from_pretrained("imagegeneration@006")
            images = model.generate_images(prompt=prompt, number_of_images=1, width=1024, height=1024)
            if images:
                img = images[0]
                img.save("temp_render.png")
                with open("temp_render.png", 'rb') as f:
                    return f.read()
            return None
        except:
            return None
    
    def _save_image(self, image_bytes):
        output_dir = Path("renders")
        output_dir.mkdir(exist_ok=True)
        filename = f"render_{int(time.time())}.png"
        with open(output_dir / filename, 'wb') as f:
            f.write(image_bytes)
        return str(output_dir / filename)
"""

html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Design Studio</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Segoe UI,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}.container{background:white;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.3);max-width:800px;width:100%;padding:40px}h1{color:#333;font-size:2.5em;margin-bottom:10px}.subtitle{color:#666;font-size:1.1em}.section{margin-bottom:30px}.section-title{color:#333;font-size:1.3em;margin-bottom:15px;font-weight:600}.file-btn{display:block;background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:15px 30px;border-radius:8px;cursor:pointer;text-align:center;font-size:1.1em;font-weight:600;width:100%;border:none}input[type=file]{display:none}#filename{display:block;margin-top:10px;padding:10px;background:#f0f0f0;border-radius:6px;text-align:center;color:#666}.options-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}label{color:#333;font-weight:500;margin-bottom:8px}select,textarea,input[type=text]{padding:10px;border:2px solid #ddd;border-radius:6px;font-size:.95em;width:100%}.render-btn{width:100%;background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:15px 30px;border:none;border-radius:8px;font-size:1.1em;font-weight:600;cursor:pointer}.render-btn:disabled{opacity:.6;cursor:not-allowed}.loading{display:none;text-align:center;color:#666;margin-top:20px}.loading.active{display:block}.spinner{border:4px solid #f3f3f3;border-top:4px solid #667eea;border-radius:50%;width:40px;height:40px;animation:spin 1s linear infinite;margin:0 auto 10px}@keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}.result{display:none;text-align:center;margin-top:30px;padding:20px;background:#f9f9f9;border-radius:8px}.result.active{display:block}.result img{max-width:100%;border-radius:8px;margin:20px 0}.error{display:none;padding:15px;background:#fee;color:#c33;border-radius:6px}.error.active{display:block}</style></head><body><div class="container"><header><h1>🎨 Design Studio</h1><p class="subtitle">AI Render from 3D Models</p></header><form id="renderForm"><div class="section"><div class="section-title">1. Upload File (DAE, GLB, OBJ)</div><label for="fileInput" class="file-btn">📁 Choose File</label><input type="file" id="fileInput" accept=".dae,.glb,.obj"><div id="filename">No file selected</div></div><div class="section"><div class="section-title">2. Rendering Options</div><div class="options-grid"><div><label>☀️ Lighting</label><select id="lighting"><option value="interior_daylight">Interior Daylight</option></select></div><div><label>🎨 Style</label><select id="style"><option value="Photorealistic" selected>Photorealistic</option></select></div></div></div><button type="submit" class="render-btn" id="renderBtn">🎬 RENDER IMAGE</button></form><div class="loading" id="loading"><div class="spinner"></div><p>Generating...</p></div><div class="error" id="error"></div><div class="result" id="result"><h3>✅ Done!</h3><img id="resultImage" src=""><a href="#" id="downloadBtn" download>📥 Download</a></div></div><script>const fileInput=document.getElementById('fileInput');const filenameDisplay=document.getElementById('filename');const renderForm=document.getElementById('renderForm');const renderBtn=document.getElementById('renderBtn');const loading=document.getElementById('loading');const error=document.getElementById('error');const result=document.getElementById('result');const resultImage=document.getElementById('resultImage');const downloadBtn=document.getElementById('downloadBtn');fileInput.addEventListener('change',(e)=>{if(e.target.files[0]){filenameDisplay.textContent=`✓ ${e.target.files[0].name}`;}});renderForm.addEventListener('submit',async(e)=>{e.preventDefault();if(!fileInput.files[0]){error.textContent='❌ Select file first';error.classList.add('active');return;}const formData=new FormData();formData.append('file',fileInput.files[0]);formData.append('lighting',document.getElementById('lighting').value);formData.append('style',document.getElementById('style').value);renderBtn.disabled=true;loading.classList.add('active');error.classList.remove('active');result.classList.remove('active');try{const uploadRes=await fetch('/api/upload',{method:'POST',body:formData});if(!uploadRes.ok) throw new Error('Upload failed');const uploadData=await uploadRes.json();const renderFormData=new FormData();renderFormData.append('filename',uploadData.filename);renderFormData.append('lighting',document.getElementById('lighting').value);renderFormData.append('style',document.getElementById('style').value);const renderRes=await fetch('/api/render',{method:'POST',body:renderFormData});if(!renderRes.ok) throw new Error('Render failed');const blob=await renderRes.blob();const url=URL.createObjectURL(blob);resultImage.src=url;downloadBtn.href=url;result.classList.add('active');}catch(err){error.textContent=`❌ ${err.message}`;error.classList.add('active');}finally{renderBtn.disabled=false;loading.classList.remove('active');}});</script></body></html>"""

# Write files
files = {
    "backend\\main.py": main_py,
    "backend\\database.py": database_py,
    "backend\\core\\__init__.py": "",
    "backend\\core\\dae_parser.py": dae_parser_py,
    "backend\\core\\imagen_renderer.py": imagen_py,
    "backend\\api\\__init__.py": "",
    "backend\\api\\routes.py": routes_py,
    "frontend\\index.html": html
}

for filepath, content in files.items():
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {filepath}")

# Install dependencies
print("\n[3/3] Installing dependencies...")
os.system('pip install -q fastapi uvicorn google-cloud-aiplatform python-dotenv sqlalchemy pillow python-multipart')

print("\n" + "=" * 50)
print("✅ Setup Complete!")
print("=" * 50)
print("\nRun server with:")
print("  python -m uvicorn backend.main:app --reload")
print("\nThen open:")
print("  http://localhost:8000/static/index.html")
print("\n" + "=" * 50)