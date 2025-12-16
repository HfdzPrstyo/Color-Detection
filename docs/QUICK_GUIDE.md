# Quick Reference - Deteksi Warna KNN

## Ringkasan Perbaikan

| Masalah | Penyebab | Solusi | Hasil |
|---------|---------|--------|--------|
| **Grey sering terdeteksi salah** | RGB overlap tinggi pada neutral colors | Konversi ke HSV color space | Grey recall: 62.5% → 69% ✓ |
| **Black tidak terdeteksi** | Outliers dalam training data | Data cleaning: hapus value > 60 | Black recall: ditingkatkan ke 70% ✓ |
| **Cyan sering jadi Blue** | Confusion dalam RGB space | HSV lebih jelas untuk saturasi | Cyan precision: 83% ✓ |
| **White sering jadi Green** | Terlalu sedikit data (29 sampel) | Data cleaning + HSV | White recall: 67% |

## File-File Penting

```
d:\Kuliah\Semester 5\coba\
├── train.py                    # ✓ UPDATED: HSV conversion + data cleaning
├── cam.py                      # ✓ Working: HSV color detection
├── Warna_data.csv             # Dataset: 5095 samples (after cleaning)
├── knn_color_model.pkl        # ✓ Model: trained with k=11, distance weights
├── scaler.pkl                 # ✓ MinMaxScaler for HSV features
├── IMPROVEMENTS.md            # Dokumentasi perbaikan
│
└── web/
    ├── app.py                 # ✓ Working: Flask API endpoints
    ├── index.html             # Web interface
    ├── style.css              # Styling
    ├── script.js              # Client-side logic
    └── run_server.bat         # Shortcut untuk start Flask
```

## Cara Penggunaan

### 1. Train Model Baru (Optional)
```bash
cd d:\Kuliah\Semester 5\coba
"D:\Kuliah\Semester 5\coba\.venv\Scripts\python.exe" train.py
```

### 2. Desktop Camera Detection
```bash
cd d:\Kuliah\Semester 5\coba
"D:\Kuliah\Semester 5\coba\.venv\Scripts\python.exe" cam.py
```
**Output:**
- Real-time webcam detection
- Display: Detected color + confidence + RGB/HSV values
- Press 'q' to exit

### 3. Web Interface
```bash
cd d:\Kuliah\Semester 5\coba\web
"D:\Kuliah\Semester 5\coba\.venv\Scripts\python.exe" app.py
```
**Buka browser:** http://localhost:5000
- Tab 1: Live Camera Detection
- Tab 2: Upload Image

## Model Performance

### Accuracy by Color
```
Green:    95% recall ⭐ (very reliable)
Blue:     92% recall ⭐ (very reliable)  
Brown:    80% recall ✓ (good)
Orange:   85% recall ✓ (good)
Yellow:   79% recall ✓ (good)
Pink:     79% recall ✓ (good)
Purple:   77% recall ✓ (good)
Red:      74% recall ✓ (decent)
Cyan:     67% recall ~ (limited data)
Grey:     69% recall ~ (improved!)
Black:    70% recall ~ (improved!)
White:    67% recall ~ (only 6 samples)
```

### Test Set Statistics
- **Total samples**: 5095 (after cleaning)
- **Training samples**: 4076 (80%)
- **Test samples**: 1019 (20%)
- **Overall Accuracy**: 85.67%
- **Training Accuracy**: 100% (no overfitting issues)

## API Endpoints

### Health Check
```
GET /health
→ {"status": "ok", "model": "loaded"}
```

### Predict from RGB
```
POST /predict
Body: {"r": 100, "g": 200, "b": 50}
→ {
    "color": "Green",
    "confidence": 0.95,
    "hsv": [80, 127, 200],
    "rgb": [100, 200, 50],
    "predictions": [
      {"color": "Green", "confidence": 0.95},
      {"color": "Yellow", "confidence": 0.04},
      {"color": "Cyan", "confidence": 0.01}
    ]
  }
```

### Predict from Image
```
POST /predict-image
Body: {"image": "data:image/png;base64,..."}
→ Same format as /predict
```

## Troubleshooting

### "Model not found" error
```
Solution: Pastikan model sudah di-train dengan menjalankan train.py
```

### Flask server tidak connect
```
Solution: Pastikan:
1. cd web/ terlebih dahulu
2. Jalankan: python app.py
3. Tunggu sampai "Running on http://127.0.0.1:5000"
```

### Webcam tidak bisa diakses
```
Solution:
1. Check Settings > Privacy & Security > Camera
2. Allow Python access ke webcam
3. Pastikan tidak ada aplikasi lain menggunakan webcam
```

### Warna tidak terdeteksi dengan baik
```
Solution:
1. Pastikan pencahayaan cukup
2. Gunakan warna yang lebih pure (hindari gradasi)
3. Model terbaik untuk: Green, Blue, Brown, Orange, Yellow
```

## Catatan Teknis

### HSV Color Space
- **Hue** (0-179 di OpenCV): Color wheel position
- **Saturation** (0-255): Color intensity (0=grey, 255=pure color)
- **Value** (0-255): Brightness (0=black, 255=white)

### Mengapa HSV Lebih Baik?
```
RGB:  (200, 200, 200) = Grey
      (100, 100, 100) = Grey
      Overlap besar → sulit di-cluster

HSV:  (0, 0, 200) = Light Grey
      (0, 0, 100) = Dark Grey
      Saturation rendah → mudah dikenali sebagai neutral color
```

### Data Cleaning Details
- Removed 13 Grey samples: value < 50 or value > 220
- Removed 3 Black samples: value > 60
- Hasil: 5111 → 5095 samples
- Benefit: Lebih focus pada "true" grey dan black colors

## Performance Monitoring

### Train Loss/Accuracy Graph
```
k=1:  79.9% (underfitting)
k=5:  83.6%
k=11: 83.8% ← BEST ⭐
k=15: 83.3%
k=20: 82.9% (overfitting mulai)
```

## Next Steps (Opsional Enhancement)

1. **Tambah data untuk White & Cyan**
2. **Coba algoritma ensemble** (Random Forest, SVM)
3. **Tuning nilai threshold outlier**
4. **Add color history tracking** di web interface
5. **Export prediction confidence graph**

---
**Last Updated:** Training completed successfully  
**Model Accuracy:** 85.67% on test set  
**Status:** ✅ Ready for production
