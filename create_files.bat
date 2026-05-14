@echo off
setlocal enabledelayedexpansion

echo Creating all Python files...

REM Create main.py
(
echo from fastapi import FastAPI
echo from fastapi.staticfiles import StaticFiles
echo from fastapi.middleware.cors import CORSMiddleware
echo from pathlib import Path
echo import os
echo from dotenv import load_dotenv
echo.
echo load_dotenv(^)
echo.
echo from api.routes import router
echo from database import init_db
echo.
echo app = FastAPI(title="Design Studio Web API", version="1.0.0"^)
echo.
echo app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]^)
echo.
echo init_db(^)
echo app.include_router(router^)
echo.
echo frontend_path = Path(__file__^).parent.parent / "frontend"
echo if frontend_path.exists(^):
echo     app.mount("/static", StaticFiles(directory=str(frontend_path^)^), name="static"^)
echo.
echo @app.get("/"^)
echo async def root(^):
echo     return {"service": "Design Studio Web API", "version": "1.0.0", "status": "running"}
echo.
echo @app.on_event("startup"^)
echo async def startup_event(^):
echo     print("=" * 50^)
echo     print("🎨 Design Studio Web API"^)
echo     print("=" * 50^)
echo     print("✓ Ready for requests"^)
echo     print("=" * 50^)
echo.
echo if __name__ == "__main__":
echo     import uvicorn
echo     uvicorn.run(app, host="0.0.0.0", port=8000^)
) > backend\main.py

echo ✓ main.py created

REM Create database.py
(
echo from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
echo from sqlalchemy.ext.declarative import declarative_base
echo from sqlalchemy.orm import sessionmaker
echo from datetime import datetime
echo.
echo DATABASE_URL = "sqlite:///./design_studio.db"
echo engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}^)
echo SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine^)
echo Base = declarative_base(^)
echo.
echo class User(Base^):
echo     __tablename__ = "users"
echo     id = Column(Integer, primary_key=True, index=True^)
echo.
echo class Project(Base^):
echo     __tablename__ = "projects"
echo     id = Column(Integer, primary_key=True, index=True^)
echo.
echo class Render(Base^):
echo     __tablename__ = "renders"
echo     id = Column(Integer, primary_key=True, index=True^)
echo.
echo Session = SessionLocal
echo.
echo def init_db(^):
echo     Base.metadata.create_all(bind=engine^)
) > backend\database.py

echo ✓ database.py created

REM Create __init__ files
echo. > backend\core\__init__.py
echo. > backend\api\__init__.py

echo ✓ __init__.py files created

REM Copy other files (simplified versions)
REM For now, create minimal versions

(
echo import xml.etree.ElementTree as ET
echo from pathlib import Path
echo.
echo class DAEParser:
echo     def __init__(self, filepath^):
echo         self.filepath = Path(filepath^)
echo         self.data = {"cameras": [], "meshes": [], "materials": [], "lights": [], "metadata": {"filename": self.filepath.name, "format": ".dae"}}
echo.
echo     def parse(self^) -^> bool:
echo         try:
echo             tree = ET.parse(self.filepath^)
echo             root = tree.getroot(^)
echo             ns = {'dae': 'http://www.collada.org/2005/11/COLLADASchema'}
echo             for camera in root.findall('.//dae:camera', ns^):
echo                 self.data['cameras'].append({'name': camera.get('id', 'Camera'^)^)
echo             for geometry in root.findall('.//dae:geometry', ns^):
echo                 self.data['meshes'].append({'name': geometry.get('id', 'Mesh'^)^)
echo             for material in root.findall('.//dae:material', ns^):
echo                 self.data['materials'].append({'name': material.get('id', 'Material'^)^)
echo             return len(self.data['meshes'^]) ^> 0
echo         except:
echo             return False
echo.
echo     def get_data(self^):
echo         return self.data
echo.
echo     def get_info(self^):
echo         return {"cameras": len(self.data['cameras'^]), "meshes": len(self.data['meshes'^]), "materials": len(self.data['materials'^]), "lights": len(self.data['lights'^])}
) > backend\core\dae_parser.py

echo ✓ dae_parser.py created

(
echo import os
echo from pathlib import Path
echo import time
echo.
echo class ImagenRenderer:
echo     def __init__(self^):
echo         self.project_id = "682230388029"
echo         self.location = "us-central1"
echo.
echo     def render(self, scene_data, options^):
echo         try:
echo             prompt = self._build_prompt(scene_data, options^)
echo             image_bytes = self._generate_image(prompt^)
echo             if not image_bytes:
echo                 return None
echo             output_path = self._save_image(image_bytes^)
echo             return image_bytes, output_path
echo         except Exception as e:
echo             print(f"Error: {e}"^)
echo             return None
echo.
echo     def _build_prompt(self, scene_data, options^):
echo         return f"Professional design, {options.get('style', 'Photorealistic'^)}, 4K"
echo.
echo     def _generate_image(self, prompt^):
echo         try:
echo             from vertexai.vision_models import ImageGenerationModel
echo             import vertexai
echo             vertexai.init(project=self.project_id, location=self.location^)
echo             model = ImageGenerationModel.from_pretrained("imagegeneration@006"^)
echo             images = model.generate_images(prompt=prompt, number_of_images=1, width=1024, height=1024^)
echo             if images:
echo                 img = images[0]
echo                 img.save("temp_render.png"^)
echo                 with open("temp_render.png", 'rb'^) as f:
echo                     return f.read(^)
echo             return None
echo         except:
echo             return None
echo.
echo     def _save_image(self, image_bytes^):
echo         output_dir = Path("renders"^)
echo         output_dir.mkdir(exist_ok=True^)
echo         filename = f"render_{int(time.time(^))}.png"
echo         with open(output_dir / filename, 'wb'^) as f:
echo             f.write(image_bytes^)
echo         return str(output_dir / filename^)
) > backend\core\imagen_renderer.py

echo ✓ imagen_renderer.py created

echo.
echo ========================================
echo ✅ All files created!
echo ========================================
pause
