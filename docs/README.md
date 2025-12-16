# 🎨 Color Detection KNN - Project Structure

Proyek telah diorganisir dengan struktur folder yang lebih rapi dan professional!

## 📁 Struktur Folder

```
coba/
│
├── 📂 data/                          
│   └── Warna_data.csv                # Dataset (5095 samples setelah cleaning)
│
├── 📂 training/                      
│   └── train.py                      # Script training model KNN
│
├── 📂 models/                        
│   ├── knn_color_model.pkl          # Model KNN terlatih
│   └── scaler.pkl                   # MinMaxScaler untuk normalisasi HSV
│
├── 📂 desktop/                       
│   └── cam.py                        # Aplikasi deteksi warna real-time
│
├── 📂 web/                           
│   ├── app.py                        # Flask server
│   ├── 📂 templates/
│   │   └── index.html               # HTML template (Jinja2)
│   └── 📂 static/
│       ├── style.css                # Styling
│       └── script.js                # JavaScript logic
│
└── 📄 Dokumentasi
    ├── README.md                     # File ini
    ├── STRUCTURE.md                  # Detail struktur folder
    ├── QUICK_GUIDE.md               # Quick reference
    ├── SOLUTION_SUMMARY.md          # Model improvement summary
    ├── IMPROVEMENTS.md              # Technical details
    └── REORGANIZATION_COMPLETE.md   # Reorganization notes
```

## 🚀 Quick Start

### 1. Train Model (jika belum ada models)
```bash
cd training
python train.py
```
Output: `../models/knn_color_model.pkl` dan `../models/scaler.pkl`

**Status**: Accuracy 85.67%, Grey improved to 69% recall ✓

### 2. Desktop Camera Detection
```bash
cd desktop
python cam.py
```
- Real-time webcam color detection
- Display predicted color + confidence + RGB/HSV values
- Top 3 predictions
- Press 'q' to exit

### 3. Web Interface
```bash
cd web
python app.py
# Buka browser: http://localhost:5000
```
- **Tab 1**: Live Camera Detection
- **Tab 2**: Upload Image Detection
- Dual mode detection system

---

## 🎯 Model Performance

| Color | Recall | Status |
|-------|--------|--------|
| Green | 95% | ⭐ Excellent |
| Blue | 92% | ⭐ Excellent |
| Brown | 80% | ✓ Good |
| Orange | 85% | ✓ Good |
| **Grey** | **69%** | ✓ Improved! |
| **Black** | **70%** | ✓ Improved! |

**Overall Accuracy**: 85.67% ✓

## ✨ Improvements Made

- **RGB → HSV conversion**: Better untuk neutral colors
- **Data cleaning**: Removed 16 outliers (13 Grey, 3 Black)
- **Hyperparameter tuning**: k=11, weights=distance
- **Result**: Grey accuracy improved 62.5% → 69%

---

## 🔧 Technical Details

### Color Detection Pipeline
```
RGB Input → HSV Conversion → Normalization → KNN Prediction → Output
```

### Model Details
- **Algorithm**: K-Nearest Neighbors
- **k**: 11
- **Features**: Hue, Saturation, Value (HSV)
- **Training Samples**: 5095
- **Test Accuracy**: 85.67%

### Melatih Model (opsional, sudah ada model yang disimpan):
```powershell
python train.py
```

### Menjalankan Deteksi Webcam:
```powershell
python cam.py
```

## Kontrol

- **q** - Exit aplikasi
- ROI box di tengah - area untuk ambil sampel warna

## Model Details

- **Algoritma**: K-Nearest Neighbors (KNN)
- **Feature Space**: HSV (Hue, Saturation, Value)
- **Best k**: 11
- **Overall Accuracy**: 86%
- **Grey Accuracy**: 68.8% (improved dari 57.1%)
- **Black Accuracy**: 70.0%

## Data Cleaning yang Diterapkan

- Menghapus 13 outlier Grey (value < 50 atau > 220)
- Menghapus 3 outlier Black (value > 60)
- Total training: 5095 sampel (dari 5111)

## Classes yang Didukung

Black, Blue, Brown, Cyan, Green, Grey, Orange, Pink, Purple, Red, White, Yellow

## Troubleshooting

### Error: "Tidak bisa membuka webcam"
- Pastikan webcam tersambung
- Cek permission kamera di Windows Settings

### Error: "ModuleNotFoundError"
- Jalankan: `pip install -r requirements.txt`

### Model tidak akurat
- Pastikan pencahayaan cukup
- ROI harus fokus pada warna yang ingin dideteksi
- Jika diperlukan, latih ulang model dengan dataset baru

## Performance Tips

1. **Better Accuracy**: Gunakan pencahayaan yang stabil
2. **Faster Detection**: Kurangi ukuran ROI atau resolution
3. **More Stable**: Rata-ratakan prediksi dari 3-5 frame terakhir

---
Dataset: 5111 sampel warna dari berbagai kategori
Last Updated: 7 Desember 2025
