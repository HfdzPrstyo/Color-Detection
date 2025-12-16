# Struktur Proyek Terorganisir

## 📁 Folder Structure

```
d:\Kuliah\Semester 5\coba\
│
├── 📂 data/                          # Dataset
│   └── Warna_data.csv               # Training data (pindahkan di sini)
│
├── 📂 training/                     # Training scripts
│   └── train.py                     # ✓ Script untuk train model
│
├── 📂 models/                       # Trained models (auto-generated)
│   ├── knn_color_model.pkl         # ✓ Model KNN
│   └── scaler.pkl                  # ✓ MinMax Scaler
│
├── 📂 desktop/                      # Desktop application
│   └── cam.py                       # ✓ Webcam detection app
│
├── 📂 web/                          # Web application (Flask)
│   ├── app.py                       # ✓ Flask server (updated)
│   ├── 📂 templates/
│   │   └── index.html              # ✓ HTML template (moved)
│   └── 📂 static/
│       ├── style.css               # ✓ CSS stylesheet (moved)
│       └── script.js               # ✓ JavaScript (moved)
│
├── 📄 README.md
├── 📄 SOLUTION_SUMMARY.md
├── 📄 QUICK_GUIDE.md
└── 📄 IMPROVEMENTS.md
```

## 🔄 Perubahan dari Struktur Lama

| Aspek | Sebelum | Sesudah |
|-------|---------|---------|
| **Training** | `train.py` di root | `training/train.py` |
| **Models** | Disimpan di root | `models/` folder |
| **Desktop App** | `cam.py` di root | `desktop/cam.py` |
| **Web HTML** | `web/index.html` | `web/templates/index.html` |
| **Web CSS** | `web/style.css` | `web/static/style.css` |
| **Web JS** | `web/script.js` | `web/static/script.js` |
| **Dataset** | Di root | `data/` folder |
| **Model Paths** | Updated | Automatic (relative paths) |

## 🚀 Cara Menggunakan

### 1. Setup Data
```bash
# Copy Warna_data.csv ke folder data/
cp Warna_data.csv data/Warna_data.csv
```

### 2. Train Model
```bash
cd training
python train.py
# Output: ../models/knn_color_model.pkl dan ../models/scaler.pkl
```

### 3. Desktop Camera Detection
```bash
cd desktop
python cam.py
```
- Automatic load dari `../models/`
- Press 'q' untuk exit

### 4. Web Interface
```bash
cd web
python app.py
# Buka: http://localhost:5000
```
- Automatic load dari `../models/templates/` dan `../static/`
- Dual tabs: Live Camera & Upload Image

## 📝 File Paths (Automatic Relative)

### Training (training/train.py)
```python
MODELS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'models'
)
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'data'
)
# Output: d:\Kuliah\Semester 5\coba\models\
# Input: d:\Kuliah\Semester 5\coba\data\
```

### Desktop (desktop/cam.py)
```python
MODELS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'models'
)
# Load: d:\Kuliah\Semester 5\coba\models\
```

### Web (web/app.py)
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
# Load: d:\Kuliah\Semester 5\coba\models\
```

### Web Templates & Static
```python
# app.py
app = Flask(__name__, 
    template_folder='templates', 
    static_folder='static'
)
# Serve: web/templates/index.html
# Serve: web/static/style.css, script.js
```

## ✅ Keuntungan Struktur Baru

| Keuntungan | Deskripsi |
|-----------|----------|
| **Terpisah** | Setiap komponen di folder sendiri |
| **Scalable** | Mudah tambah fitur baru |
| **Maintainable** | Mudah dipahami struktur |
| **Professional** | Follow best practices |
| **Modular** | Bisa reuse code di project lain |
| **Auto Paths** | Paths relatif (portable) |

## 📋 Quick Checklist

- [ ] Copy `Warna_data.csv` ke folder `data/`
- [ ] Jalankan `training/train.py` untuk generate models
- [ ] Verify `models/knn_color_model.pkl` dan `models/scaler.pkl` tercipta
- [ ] Test desktop: `python desktop/cam.py`
- [ ] Test web: `cd web && python app.py`
- [ ] Buka http://localhost:5000

## 🔧 Troubleshooting

### "Model not found" error
```
✓ Pastikan models folder berisi:
  - knn_color_model.pkl
  - scaler.pkl
✓ Jalankan: training/train.py
```

### "Templates folder not found"
```
✓ Pastikan struktur web/:
  - web/templates/index.html
  - web/static/style.css
  - web/static/script.js
✓ Run dari folder root, bukan web/
```

### Path errors
```
✓ Gunakan relative paths (sudah automatic)
✓ Jangan hardcode absolute paths
```

## 📚 Related Files

- `IMPROVEMENTS.md` - Technical details tentang model optimization
- `QUICK_GUIDE.md` - Quick reference untuk semua fitur
- `SOLUTION_SUMMARY.md` - Complete solution documentation
- `README.md` - General project overview

## 🎯 Next Steps

1. **Verify all folders created**
   ```bash
   tree /F
   ```

2. **Copy dataset**
   ```bash
   copy Warna_data.csv data\
   ```

3. **Train model**
   ```bash
   cd training && python train.py
   ```

4. **Test all features**
   - Desktop: `cd desktop && python cam.py`
   - Web: `cd web && python app.py`
