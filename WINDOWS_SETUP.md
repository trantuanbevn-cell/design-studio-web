# 🎨 Design Studio Web - Windows Setup

## 🚀 Super Simple - 2 Steps!

### **Step 1: Setup (1 minute)**

Double-click: **`SETUP_ALL.bat`**

This will:
- ✅ Create all folders
- ✅ Create all Python files  
- ✅ Install dependencies
- ✅ Done!

### **Step 2: Run Server**

Double-click: **`run.bat`**

You'll see:
```
========================================
🎨 Design Studio Web API
========================================
✓ Server running at:
   http://localhost:8000/static/index.html
========================================
```

### **Step 3: Open Browser**

Click this link or paste in browser:
```
http://localhost:8000/static/index.html
```

---

## 📋 What It Does

| File | Purpose |
|------|---------|
| `SETUP_ALL.bat` | **Run FIRST** - Creates everything |
| `run.bat` | **Run SECOND** - Starts server |
| `create_files.bat` | Creates Python files (used by SETUP_ALL) |
| `create_routes.bat` | Creates routes.py (used by SETUP_ALL) |
| `create_frontend.bat` | Creates HTML (used by SETUP_ALL) |
| `install.bat` | Manual install (if needed) |

---

## 🧪 Test Workflow

1. Upload `.dae` file
2. Select lighting/style
3. Click **RENDER IMAGE**
4. Wait 30-60 seconds
5. See image! ✅

---

## ⚠️ Troubleshooting

### "Command not recognized"
→ Make sure you're in the right folder:
```
cd D:\design-studio-web
```

### "Python not found"
→ Install Python from python.org (add to PATH)

### Port 8000 already in use
→ Edit `run.bat`, change `--port 8000` to `--port 8001`

### Dependencies fail
→ Run manually:
```
pip install fastapi uvicorn google-cloud-aiplatform python-dotenv sqlalchemy pillow python-multipart
```

---

## 📂 Folder Structure (After Setup)

```
design-studio-web\
├── backend\
│   ├── core\
│   │   ├── dae_parser.py
│   │   ├── imagen_renderer.py
│   │   └── __init__.py
│   ├── api\
│   │   ├── routes.py
│   │   └── __init__.py
│   ├── main.py
│   └── database.py
├── frontend\
│   └── index.html
├── uploads\
├── renders\
├── SETUP_ALL.bat
├── run.bat
└── design_studio.db (created after first run)
```

---

## 🎯 That's It!

- `SETUP_ALL.bat` → `run.bat` → **http://localhost:8000**

**Enjoy!** 🎨
