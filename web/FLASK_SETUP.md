# FLASK SERVER TROUBLESHOOTING & FIX

## ✅ Perbaikan yang Sudah Dilakukan

### Masalah 1: Model File Not Found
**Error**: `FileNotFoundError: knn_color_model.pkl not found`
**Cause**: Flask mencari file di folder `web/` tapi model ada di folder root
**Fix**: Update `app.py` untuk menggunakan path absolut ke parent directory

### Masalah 2: Flask Module Not Installed
**Error**: `ModuleNotFoundError: No module named 'flask'`
**Cause**: Flask belum terinstall di virtual environment
**Fix**: Install dengan: `pip install flask flask-cors`

---

## 🚀 Cara Menjalankan Flask Server (3 Cara)

### CARA 1: Using Batch File (RECOMMENDED - Windows)
**Step 1**: Double-click `web/run_server.bat`
- Otomatis activate venv
- Otomatis jalankan app.py
- Error handling built-in

**Expected output**:
```
Loading model and scaler...
Looking for model in: d:\Kuliah\Semester 5\coba
Model path: d:\Kuliah\Semester 5\coba\knn_color_model.pkl
Scaler path: d:\Kuliah\Semester 5\coba\scaler.pkl
Model loaded successfully!
 * Running on http://0.0.0.0:5000
```

---

### CARA 2: Manual via PowerShell
**Step 1**: Open PowerShell

**Step 2**: Activate venv
```powershell
cd "d:\Kuliah\Semester 5\coba"
.\.venv\Scripts\Activate.ps1
```

**Step 3**: Change to web folder dan run app
```powershell
cd web
python app.py
```

**Expected output**: (same seperti Cara 1)

---

### CARA 3: Run dari VS Code Terminal
**Step 1**: Open VS Code integrated terminal
- View → Terminal (atau Ctrl + `)

**Step 2**: Activate venv
```powershell
.\.venv\Scripts\Activate.ps1
```

**Step 3**: Change to web folder dan run
```powershell
cd web
python app.py
```

---

## ✅ Verification - Semua API Endpoints Working

| Endpoint | Method | Input | Status |
|----------|--------|-------|--------|
| `/health` | GET | - | ✅ 200 OK |
| `/predict` | POST | `{r,g,b}` | ✅ 200 OK |
| `/info` | GET | - | ✅ 200 OK |

### Test Response Example:
```json
{
  "color": "Green",
  "confidence": 1.0,
  "hsv": [47, 127, 200],
  "rgb": [145, 200, 100],
  "predictions": [
    {"color": "Green", "confidence": 1.0},
    {"color": "Yellow", "confidence": 0.0},
    {"color": "Red", "confidence": 0.0}
  ]
}
```

---

## 🔍 Debug: Jika Server Tetap Error

### 1. Check Virtual Environment Activated
```powershell
# Should show (.venv) di prompt
echo $PROFILE
```

### 2. Check Flask Installed
```powershell
pip list | grep flask
# Should show: flask, flask-cors
```

### 3. Check Model Files Exist
```powershell
# Di folder root (d:\Kuliah\Semester 5\coba)
ls *.pkl
# Should show:
#   knn_color_model.pkl
#   scaler.pkl
```

### 4. Check Correct Working Directory
Saat run `python app.py`:
```powershell
# Harus di dalam folder web/
cd d:\Kuliah\Semester 5\coba\web
python app.py
```

### 5. Manual Test API
Jika server running, test di terminal lain:
```powershell
# Test /health
curl http://localhost:5000/health

# Test /predict
$body = @{r=145; g=200; b=100} | ConvertTo-Json
curl -X POST http://localhost:5000/predict `
  -H "Content-Type: application/json" `
  -d $body
```

---

## 🛠️ File yang Sudah Diperbaiki

### app.py Changes:
```python
# BEFORE (ERROR):
model = joblib.load("knn_color_model.pkl")
scaler = joblib.load("scaler.pkl")

# AFTER (FIXED):
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "knn_color_model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
```

---

## 📋 Checklist Sebelum Jalankan

- [ ] Virtual environment activated (`.venv`)
- [ ] Flask & flask-cors installed (`pip install flask flask-cors`)
- [ ] Model files exist:
  - [ ] `d:\Kuliah\Semester 5\coba\knn_color_model.pkl`
  - [ ] `d:\Kuliah\Semester 5\coba\scaler.pkl`
- [ ] Working directory: `d:\Kuliah\Semester 5\coba\web` (saat run app.py)
- [ ] Port 5000 available (tidak digunakan aplikasi lain)

---

## 🎯 Full Setup + Run Sequence

```powershell
# 1. Open PowerShell di folder project
cd "d:\Kuliah\Semester 5\coba"

# 2. Activate venv (if not already)
.\.venv\Scripts\Activate.ps1

# 3. Install Flask (if not already)
pip install flask flask-cors

# 4. Go to web folder
cd web

# 5. Run Flask server
python app.py

# 6. In another PowerShell, test
curl http://localhost:5000/health
```

---

## 🌐 Web App Connection

Jika Flask server running di port 5000:

1. **Open web app** (dalam browser):
   - File URL: `file:///d:/Kuliah/Semester%205/coba/web/index.html`
   - Live Server: `http://127.0.0.1:5500` (jika pakai Live Server extension)
   - HTTP Server: `http://localhost:3000` (jika pakai `python -m http.server 3000`)

2. **Check API status** di web app:
   - Akan muncul status "Connected to server" atau "Server not connected"
   - Jika "not connected": pastikan Flask server running

3. **Start detecting**:
   - Klik "START CAMERA"
   - Izinkan webcam access
   - Position object di ROI box
   - Hasil akan muncul real-time

---

## 🚨 Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: flask` | Flask not installed | `pip install flask flask-cors` |
| `FileNotFoundError: *.pkl` | Model not found | Check file exists in root folder |
| `Port 5000 already in use` | Another app using port | Kill other app or use different port |
| `Connection refused` | Flask not running | Start `python app.py` in web folder |
| `Webcam not working` | Browser permission | Allow camera access in browser popup |
| `CORS error` | Server not accessible | Ensure localhost:5000 reachable |

---

## 🎉 Status

✅ Flask app fully working
✅ All endpoints tested and verified
✅ Model loading correctly
✅ API responses valid

**Ready to use!**

---

**Last Updated**: 7 Desember 2025
**Version**: 1.0 (Fixed)
