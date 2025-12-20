# 📖 Panduan Setup & Menjalankan Aplikasi

## 🎯 Tujuan
Menjalankan Color Detection Web App dengan fitur **Switch Camera** (depan/belakang) yang baru ditambahkan.

---

## 📋 Status Implementasi Fitur

✅ **SELESAI** - Semua kode sudah diupdate:
- `static/script.js` - Logika switch camera
- `templates/index.html` - Tombol dan UI
- `static/style.css` - Styling
- Dokumentasi lengkap

---

## 🛠️ Setup (Pilih salah satu)

### **METODE 1: Recommended - Gunakan Python Official**

1. **Download & Install Python 3.11** (JANGAN 3.14, ada issue dengan numpy)
   - Download dari: https://www.python.org/downloads/
   - Pilih Python 3.11 LTS
   - ✅ Check "Add Python to PATH"

2. **Buka Terminal di folder project:**
   ```bash
   cd d:\Kuliah\Semester 5\coba
   ```

3. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate Virtual Environment:**
   ```bash
   venv\Scripts\activate
   ```

5. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install opencv-python flask flask-cors pillow joblib scikit-learn
   ```

6. **Run Flask Server:**
   ```bash
   python app.py
   ```

---

### **METODE 2: Gunakan Miniconda (Lebih Mudah)**

1. **Download Miniconda** dari: https://docs.conda.io/projects/miniconda/en/latest/
   - Pilih **Miniconda3 Latest**

2. **Buka "Anaconda Prompt"** (bukan PowerShell)

3. **Navigate ke folder:**
   ```bash
   cd d:\Kuliah\Semester 5\coba
   ```

4. **Create conda environment:**
   ```bash
   conda create -n colordetect python=3.11 -y
   ```

5. **Activate environment:**
   ```bash
   conda activate colordetect
   ```

6. **Install packages:**
   ```bash
   conda install -c conda-forge opencv flask flask-cors pillow joblib scikit-learn -y
   ```

7. **Run app:**
   ```bash
   python app.py
   ```

---

### **METODE 3: Skip OpenCV - Gunakan PIL saja**

Jika tidak bisa install OpenCV, edit `app.py`:

```python
# Hapus atau comment ini:
# import cv2

# Gunakan PIL sebaliknya untuk color conversion
from PIL import Image
```

Kemudian install hanya:
```bash
pip install flask flask-cors pillow joblib scikit-learn
```

---

## ✅ Verifikasi Server Berjalan

Ketika server running, Anda akan melihat:
```
Loading model and scaler...
Model loaded successfully!
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## 🌐 Akses Aplikasi

Buka browser dan pergi ke:
```
http://localhost:5000
```

---

## 🎥 Gunakan Fitur Kamera Belakang

1. **Klik "START CAMERA"**
   - Kamera depan akan menyala
   - Label menunjukkan "Front Camera"

2. **Klik "🔄 Switch Camera"**
   - Beralih ke kamera belakang (jika tersedia)
   - Label berubah menjadi "Rear Camera"

3. **Klik lagi untuk kembali**
   - Switch kembali ke kamera depan

---

## 🐛 Troubleshooting

### ❌ Error: "ModuleNotFoundError: No module named 'cv2'"
**Solusi:**
```bash
# Pastikan virtual env activated
# Cek dengan: where python (seharusnya di folder venv)

# Install ulang opencv
pip install --upgrade --force-reinstall opencv-python

# Atau gunakan OpenCV headless (lebih ringan)
pip install opencv-python-headless
```

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"
**Solusi:**
```bash
pip install flask flask-cors
```

### ❌ Error: "Model not found"
**Solusi:**
- Pastikan folder `models/` ada
- Jalankan training: `cd training && python train.py && cd ..`

### ❌ "Camera not available"
**Penyebab:** 
- Browser tidak diberikan permission
- Kamera sedang digunakan aplikasi lain

**Solusi:**
- Refresh halaman dan klik "Allow"
- Tutup aplikasi lain yang pakai kamera

### ❌ Switch Camera button tidak berfungsi
**Penyebab:** JavaScript error
**Solusi:**
- Buka DevTools (F12)
- Lihat Console tab untuk error message
- Refresh halaman

---

## 📝 Quick Start (Single Command)

**Windows - PowerShell:**
```powershell
cd 'd:\Kuliah\Semester 5\coba'; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install opencv-python flask flask-cors pillow joblib scikit-learn; python app.py
```

**Windows - CMD:**
```cmd
cd d:\Kuliah\Semester 5\coba && python -m venv venv && venv\Scripts\activate.bat && pip install opencv-python flask flask-cors pillow joblib scikit-learn && python app.py
```

---

## 📂 Folder Structure

```
coba/
├── app.py                          ← RUN THIS FILE
├── requirements.txt
├── run_server.bat                  ← Atau double-click ini
├── templates/
│   └── index.html                  ✅ Updated
├── static/
│   ├── script.js                   ✅ Updated (Switch Camera Logic)
│   ├── style.css                   ✅ Updated (Styling)
├── models/
│   ├── knn_color_model.pkl
│   └── scaler.pkl
├── data/
│   └── Warna_data.csv
└── training/
    ├── train.py
    └── requirements.txt
```

---

## 🎯 Checklist Sebelum Test

- [ ] Python 3.11+ terinstall
- [ ] Virtual environment dibuat
- [ ] Dependencies terinstall
- [ ] Model files ada di folder `models/`
- [ ] Terminal bisa akses Flask (tidak error)
- [ ] Browser bisa akses `localhost:5000`

---

## 🚀 Fitur yang Siap

| Fitur | Status |
|-------|--------|
| Live Camera Feed | ✅ |
| Switch Front/Rear Camera | ✅ NEW |
| Real-time Color Detection | ✅ |
| Image Upload | ✅ |
| RGB/HSV Display | ✅ |
| Top 3 Predictions | ✅ |
| Confidence Score | ✅ |

---

## 💡 Tips & Tricks

- **Deteksi lebih akurat?** Pastikan pencahayaan bagus di sekitar object
- **Ubah kecepatan deteksi?** Edit `FRAME_INTERVAL_MS` di `script.js` (default 3000ms)
- **Pakai kamera eksternal?** Browser akan auto-detect jika tersedia

---

## 📞 Bantuan

Jika masih error setelah ikuti semua langkah:

1. **Check Python version:**
   ```bash
   python --version
   ```
   (Seharusnya 3.11 atau lebih tinggi, maksimal 3.12 untuk compatibility)

2. **Check installed packages:**
   ```bash
   pip list
   ```
   (Pastikan ada: flask, opencv-python, joblib, scikit-learn, numpy)

3. **Check port 5000:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   ```
   (Jika ada, port sedang terpakai, gunakan port lain)

4. **Lihat error di browser console:**
   - Buka DevTools (F12)
   - Tab "Console"
   - Catat semua error message

---

## ✨ Enjoy Your App!

Setelah semua setup selesai, aplikasi siap dengan fitur **Switch Camera** yang baru. Selamat mencoba! 🎉
