# QUICK START - Color Detection Web Application

Panduan cepat untuk menjalankan aplikasi web color detection dengan KNN model.

## 📋 Requirement

- Python 3.9+
- Browser modern (Chrome, Firefox, Edge)
- Webcam
- Port 5000 dan 3000 tersedia

## 🚀 Cara Menjalankan (Windows)

### Step 1: Setup (Hanya pertama kali)

Double-click file `setup.bat` di folder `web/`:
```
web/setup.bat
```

Ini akan:
- Membuat virtual environment
- Install Flask, CORS, dan dependencies lainnya

### Step 2: Start Flask Server

Double-click file `run_server.bat` di folder `web/`:
```
web/run_server.bat
```

Jika sukses, akan muncul:
```
Loading model and scaler...
Model loaded successfully!
 * Running on http://0.0.0.0:5000
```

**JANGAN TUTUP TERMINAL INI! Biarkan tetap berjalan.**

### Step 3: Buka Web App di Browser

Pilih salah satu cara:

#### Cara A: Manual (Recommended)
1. Buka VS Code
2. Klik kanan pada `index.html` di folder `web/`
3. Pilih "Open with Live Server"
4. Browser akan otomatis membuka di `http://127.0.0.1:5500`

#### Cara B: Manual via Browser
1. Buka browser (Chrome/Firefox/Edge)
2. Ketik di address bar: `file:///d:/Kuliah/Semester%205/coba/web/index.html`
3. Aplikasi akan terbuka

#### Cara C: Python HTTP Server
```powershell
cd "d:\Kuliah\Semester 5\coba\web"
python -m http.server 3000
# Buka browser ke http://localhost:3000
```

### Step 4: Mulai Deteksi

1. Klik tombol **START CAMERA**
2. Izinkan browser untuk mengakses webcam saat popup muncul
3. Posisikan objek warna di kotak hijau (ROI)
4. Hasil deteksi akan muncul di sisi kanan
5. Klik **STOP CAMERA** untuk berhenti

## 📊 Interface Penjelasan

```
┌─ WEBCAM FEED ──────────┬─ HASIL DETEKSI ────────────────┐
│                        │                                │
│   [Video dari camera]  │  Detected Color: GREEN         │
│                        │  Confidence: 95.2%             │
│   ┌─────────────┐      │  [Color Box]                   │
│   │  ┌─ ROI ─┐  │      │                                │
│   │  │ [##]  │  │      │  RGB Values:                   │
│   │  └───────┘  │      │  R: 145  G: 200  B: 100       │
│   └─────────────┘      │                                │
│                        │  HSV Values:                   │
│ [START] [STOP]         │  H: 80  S: 43  V: 159         │
│                        │                                │
│                        │  Top Predictions:             │
│                        │  1. Green: 95.2%              │
│                        │  2. Yellow: 3.1%              │
│                        │  3. Cyan: 1.7%                │
└────────────────────────┴────────────────────────────────┘
```

### Komponen:

- **WEBCAM FEED**: Video dari webcam Anda (mirror)
- **ROI Box**: Kotak hijau untuk sampling warna
- **Detected Color**: Warna yang terdeteksi oleh model KNN
- **Confidence**: Seberapa yakin model dengan prediksi (%)
- **Color Box**: Preview warna actual vs warna terdeteksi
- **RGB/HSV**: Nilai color space dari ROI
- **Top Predictions**: 3 prediksi teratas dengan probability

## 🎯 Tips Penggunaan

### Agar Deteksi Akurat:
1. ✓ Pencahayaan cukup dan merata
2. ✓ Warna fully berada dalam ROI box
3. ✓ Jangan ada shadow/bayangan pada ROI
4. ✓ Jarak camera ~20-30 cm dari objek

### Troubleshooting:

**Q: "Server not connected" error muncul**
- A: Pastikan `run_server.bat` sudah running (terminal tetap terbuka)
- A: Cek port 5000 tidak digunakan aplikasi lain

**Q: Webcam tidak terdeteksi**
- A: Izinkan browser akses webcam saat popup
- A: Check Windows Settings > Privacy > Camera
- A: Restart browser jika perlu

**Q: Hasil deteksi tidak akurat**
- A: Perbaiki pencahayaan
- A: Posisikan objek tepat di tengah ROI
- A: Model dilatih dengan HSV space, RGB mungkin berbeda

**Q: Halaman tidak bisa diakses**
- A: Pastikan Live Server running (jika pakai VS Code)
- A: Atau jalankan `python -m http.server 3000`
- A: Tunggu beberapa detik untuk halaman fully load

**Q: Script.js tidak load**
- A: Pastikan file `script.js` ada di folder `web/`
- A: Refresh browser (Ctrl+F5) untuk clear cache

## 📁 Struktur File

```
coba/
├── train.py                 # Training script
├── cam.py                   # Desktop camera app
├── knn_color_model.pkl      # Model KNN yang sudah dilatih
├── scaler.pkl               # Scaler untuk HSV normalization
├── web/
│   ├── index.html          # Halaman web (HTML)
│   ├── style.css           # Styling (CSS)
│   ├── script.js           # Logic (JavaScript)
│   ├── app.py              # Flask backend
│   ├── setup.bat           # Setup script
│   ├── run_server.bat      # Server launcher
│   └── README.md           # Full documentation
└── README.md               # Project overview
```

## 🔧 Teknologi yang Digunakan

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask, CORS
- **ML Model**: KNN (scikit-learn)
- **Image Processing**: OpenCV
- **Color Space**: HSV (dari RGB)
- **API**: RESTful JSON

## ⚙️ Configuration

### Mengubah FPS:
Edit `script.js`, cari:
```javascript
const FRAME_RATE = 30; // Ubah ke nilai lain (10-60 recommended)
```

### Mengubah ROI Size:
Edit `script.js`, cari:
```javascript
const ROI_SIZE = 120; // Ubah ukuran ROI (pixel)
```

### Mengubah API URL:
Edit `script.js`, cari:
```javascript
const API_URL = 'http://localhost:5000'; // Ubah sesuai kebutuhan
```

## 📈 Model Performance

- **Overall Accuracy**: 86%
- **Grey Accuracy**: 68.8% ↑ (improved)
- **Black Accuracy**: 70.0%
- **K Neighbors**: 11
- **Feature Space**: HSV (Hue, Saturation, Value)
- **Total Training Samples**: 5,095 (after cleaning)

## 🎓 Classes yang Didukung

12 warna: Black, Blue, Brown, Cyan, Green, Grey, Orange, Pink, Purple, Red, White, Yellow

## 📞 Support

Jika ada error atau bug:
1. Check console browser (F12 > Console)
2. Check terminal Flask server
3. Lihat file README.md yang lebih detail
4. Cek app.py untuk detail API

## ✅ Checklist Sebelum Jalankan

- [ ] Python 3.9+ terinstall
- [ ] Webcam terhubung
- [ ] Browser modern (Chrome/Firefox/Edge)
- [ ] VS Code extension "Live Server" terinstall (optional but recommended)
- [ ] File model `knn_color_model.pkl` dan `scaler.pkl` ada di root
- [ ] Port 5000 tidak sedang digunakan aplikasi lain

## 🎉 Siap!

Jika semua setup sudah selesai:
1. Jalankan `setup.bat` (pertama kali saja)
2. Jalankan `run_server.bat` (tetap running)
3. Buka `index.html` dengan Live Server
4. Klik START CAMERA dan mulai deteksi!

---

**Happy Color Detecting!** 🎨🎥

*Last Updated: 7 Desember 2025*
