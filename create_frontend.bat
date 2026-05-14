@echo off
(
echo ^<!DOCTYPE html^>
echo ^<html lang="en"^>
echo ^<head^>
echo     ^<meta charset="UTF-8"^>
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>
echo     ^<title^>Design Studio - AI Render^</title^>
echo     ^<style^>
echo         * { margin:0; padding:0; box-sizing:border-box; }
echo         body { font-family:'Segoe UI',sans-serif; background:linear-gradient(135deg,#667eea 0%%,#764ba2 100%%); min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px; }
echo         .container { background:white; border-radius:12px; box-shadow:0 20px 60px rgba(0,0,0,0.3); max-width:800px; width:100%%; padding:40px; }
echo         header { text-align:center; margin-bottom:40px; }
echo         h1 { color:#333; font-size:2.5em; margin-bottom:10px; }
echo         .subtitle { color:#666; font-size:1.1em; }
echo         .section { margin-bottom:30px; }
echo         .section-title { color:#333; font-size:1.3em; margin-bottom:15px; font-weight:600; }
echo         .file-btn { display:block; background:linear-gradient(135deg,#667eea 0%%,#764ba2 100%%); color:white; padding:15px 30px; border-radius:8px; cursor:pointer; text-align:center; font-size:1.1em; font-weight:600; width:100%%; border:none; }
echo         input[type="file"] { display:none; }
echo         .file-btn:hover { background:#667eea; }
echo         #filename { display:block; margin-top:10px; padding:10px; background:#f0f0f0; border-radius:6px; text-align:center; color:#666; }
echo         .options-grid { display:grid; grid-template-columns:1fr 1fr; gap:15px; }
echo         label { color:#333; font-weight:500; margin-bottom:8px; }
echo         select, textarea, input[type="text"] { padding:10px; border:2px solid #ddd; border-radius:6px; font-size:0.95em; width:100%%; }
echo         .render-btn { width:100%%; background:linear-gradient(135deg,#667eea 0%%,#764ba2 100%%); color:white; padding:15px 30px; border:none; border-radius:8px; font-size:1.1em; font-weight:600; cursor:pointer; }
echo         .render-btn:disabled { opacity:0.6; cursor:not-allowed; }
echo         .loading { display:none; text-align:center; color:#666; margin-top:20px; }
echo         .loading.active { display:block; }
echo         .spinner { border:4px solid #f3f3f3; border-top:4px solid #667eea; border-radius:50%%; width:40px; height:40px; animation:spin 1s linear infinite; margin:0 auto 10px; }
echo         @keyframes spin { 0%% { transform:rotate(0deg); } 100%% { transform:rotate(360deg); } }
echo         .result { display:none; text-align:center; margin-top:30px; padding:20px; background:#f9f9f9; border-radius:8px; }
echo         .result.active { display:block; }
echo         .result img { max-width:100%%; border-radius:8px; margin:20px 0; }
echo         .error { display:none; padding:15px; background:#fee; color:#c33; border-radius:6px; }
echo         .error.active { display:block; }
echo     ^</style^>
echo ^</head^>
echo ^<body^>
echo     ^<div class="container"^>
echo         ^<header^>
echo             ^<h1^>🎨 Design Studio^</h1^>
echo             ^<p class="subtitle"^>AI Render from 3D Models^</p^>
echo         ^</header^>
echo.
echo         ^<form id="renderForm"^>
echo             ^<div class="section"^>
echo                 ^<div class="section-title"^>1. Upload File (DAE, GLB, OBJ)^</div^>
echo                 ^<label for="fileInput" class="file-btn"^>📁 Choose File^</label^>
echo                 ^<input type="file" id="fileInput" accept=".dae,.glb,.obj"^>
echo                 ^<div id="filename"^>No file selected^</div^>
echo             ^</div^>
echo.
echo             ^<div class="section"^>
echo                 ^<div class="section-title"^>2. Rendering Options^</div^>
echo                 ^<div class="options-grid"^>
echo                     ^<div^>
echo                         ^<label for="lighting"^>☀️ Lighting^</label^>
echo                         ^<select id="lighting"^>
echo                             ^<option value="interior_daylight"^>Interior Daylight^</option^>
echo                             ^<option value="interior_evening"^>Evening^</option^>
echo                             ^<option value="exterior_daylight"^>Exterior^</option^>
echo                         ^</select^>
echo                     ^</div^>
echo                     ^<div^>
echo                         ^<label for="style"^>🎨 Style^</label^>
echo                         ^<select id="style"^>
echo                             ^<option value="Photorealistic" selected^>Photorealistic^</option^>
echo                             ^<option value="Modern"^>Modern^</option^>
echo                             ^<option value="Minimalist"^>Minimalist^</option^>
echo                         ^</select^>
echo                     ^</div^>
echo                     ^<div^>
echo                         ^<label for="resolution"^>📐 Resolution^</label^>
echo                         ^<select id="resolution"^>
echo                             ^<option value="2K" selected^>2K^</option^>
echo                             ^<option value="4K"^>4K^</option^>
echo                         ^</select^>
echo                     ^</div^>
echo                     ^<div^>
echo                         ^<label for="description"^>💬 Notes^</label^>
echo                         ^<input type="text" id="description" placeholder="Optional"^>
echo                     ^</div^>
echo                 ^</div^>
echo             ^</div^>
echo.
echo             ^<button type="submit" class="render-btn" id="renderBtn"^>🎬 RENDER IMAGE^</button^>
echo         ^</form^>
echo.
echo         ^<div class="loading" id="loading"^>
echo             ^<div class="spinner"^>^</div^>
echo             ^<p^>Generating... (30-60 seconds)^</p^>
echo         ^</div^>
echo.
echo         ^<div class="error" id="error"^>^</div^>
echo.
echo         ^<div class="result" id="result"^>
echo             ^<h3^>✅ Done!^</h3^>
echo             ^<img id="resultImage" src="" alt="Render"^>
echo             ^<a href="#" id="downloadBtn" download^>📥 Download^</a^>
echo         ^</div^>
echo     ^</div^>
echo.
echo     ^<script^>
echo         const fileInput=document.getElementById('fileInput');const filenameDisplay=document.getElementById('filename');const renderForm=document.getElementById('renderForm');const renderBtn=document.getElementById('renderBtn');const loading=document.getElementById('loading');const error=document.getElementById('error');const result=document.getElementById('result');const resultImage=document.getElementById('resultImage');const downloadBtn=document.getElementById('downloadBtn');fileInput.addEventListener('change',(e)=^>{const file=e.target.files[0];if(file){filenameDisplay.textContent=`✓ ${file.name}`;}^});renderForm.addEventListener('submit',async(e)=^>{e.preventDefault();if(!fileInput.files[0]){error.textContent='❌ Select file first';error.classList.add('active');return;}const formData=new FormData();formData.append('file',fileInput.files[0]);formData.append('lighting',document.getElementById('lighting').value);formData.append('style',document.getElementById('style').value);formData.append('resolution',document.getElementById('resolution').value);formData.append('description',document.getElementById('description').value);renderBtn.disabled=true;loading.classList.add('active');error.classList.remove('active');result.classList.remove('active');try{const uploadRes=await fetch('/api/upload',{method:'POST',body:formData});if(!uploadRes.ok) throw new Error('Upload failed');const uploadData=await uploadRes.json();const renderFormData=new FormData();renderFormData.append('filename',uploadData.filename);renderFormData.append('lighting',document.getElementById('lighting').value);renderFormData.append('style',document.getElementById('style').value);renderFormData.append('resolution',document.getElementById('resolution').value);renderFormData.append('description',document.getElementById('description').value);const renderRes=await fetch('/api/render',{method:'POST',body:renderFormData});if(!renderRes.ok) throw new Error('Render failed');const blob=await renderRes.blob();const url=URL.createObjectURL(blob);resultImage.src=url;downloadBtn.href=url;downloadBtn.download='render.png';result.classList.add('active');}catch(err){error.textContent=`❌ ${err.message}`;error.classList.add('active');}finally{renderBtn.disabled=false;loading.classList.remove('active');}^});
echo     ^</script^>
echo ^</body^>
echo ^</html^>
) > frontend\index.html
echo ✓ index.html created
