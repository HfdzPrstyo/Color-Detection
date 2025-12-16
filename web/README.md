# Web Color Detection - Setup & Running Guide

Aplikasi web untuk deteksi warna real-time menggunakan KNN model yang sudah dilatih.

## Struktur File

```
web/
├── index.html      # Halaman utama (HTML)
├── style.css       # Styling (CSS)
├── script.js       # Interaktif (JavaScript)
├── app.py          # Flask backend server
└── README.md       # Dokumentasi ini
```

## Persiapan

### 1. Install Dependencies Flask dan CORS

```powershell
cd "d:\Kuliah\Semester 5\coba"
.\.venv\Scripts\Activate.ps1
pip install flask flask-cors
```

### 2. Pastikan Model Sudah Ada

Model dan scaler harus tersimpan di folder root project:
- `knn_color_model.pkl`
- `scaler.pkl`

Jika belum ada, jalankan training terlebih dahulu:
```powershell
python train.py
```

## Menjalankan Aplikasi

### Terminal 1: Jalankan Flask Server

```powershell
cd "d:\Kuliah\Semester 5\coba\web"
.\..\venv\Scripts\Activate.ps1
python app.py
```

Output yang diharapkan:
```
Loading model and scaler...
Model loaded successfully!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Terminal 2: Buka Web Browser

Buka browser (Chrome, Firefox, Edge) dan akses:
```
http://localhost:3000
```

Atau jika menggunakan Live Server di VS Code:
- Klik kanan pada `index.html`
- Pilih "Open with Live Server"

## Fitur Aplikasi Web

### Dashboard Layout

```
┌─────────────────────────────────────────────────┐
│  Color Detection - Real-time KNN Recognition    │
├──────────────────┬──────────────────────────────┤
│                  │  Detected Color              │
│   WEBCAM FEED    │  ├─ Color Name               │
│   ┌──────────┐   │  ├─ Confidence %             │
│   │  ┌─ ROI ─┤   │  └─ Color Preview            │
│   │  │ [BOX] │   │                              │
│   │  └───────┤   │  RGB/HSV Values              │
│   │ START    │   │  ├─ R: 145                   │
│   │ STOP     │   │  ├─ G: 200                   │
│   └──────────┘   │  └─ B: 100                   │
│                  │                              │
│                  │  Top Predictions             │
│                  │  1. Green: 95.2%             │
│                  │  2. Yellow: 3.1%             │
│                  │  3. Cyan: 1.7%               │
└──────────────────┴──────────────────────────────┘
```

### Fitur Utama

1. **Live Webcam Feed**
   - Menampilkan video dari webcam secara real-time
   - ROI box hijau menandakan area sampling
   - Video dimirror (flipped) untuk natural feeling

2. **Color Detection**
   - Mengambil rata-rata RGB dari ROI setiap frame
   - Konversi RGB ke HSV
   - Prediksi warna menggunakan KNN model

3. **Hasil Prediksi**
   - Nama warna yang terdeteksi
   - Confidence level (%)
   - Preview warna terdeteksi vs. warna actual ROI
   - RGB values (R, G, B)
   - HSV values (H, S, V)
   - Top 3 prediksi dengan confidence

4. **Server Status**
   - Menampilkan status koneksi ke Flask server
   - Hijau = Connected, Merah = Disconnected

### Kontrol

- **START CAMERA** - Mulai webcam dan deteksi
- **STOP CAMERA** - Stop webcam
- **q** (keyboard) - Hanya untuk aplikasi desktop, tidak berlaku di web

## API Endpoints (Flask)

### Health Check
```
GET /health
Response: { "status": "ok", "model": "loaded" }
```

### Prediction
```
POST /predict
Content-Type: application/json

Request Body:
{
  "r": 145,
  "g": 200,
  "b": 100
}

Response:
{
  "color": "Green",
  "confidence": 0.952,
  "hsv": [80, 43, 159],
  "rgb": [145, 200, 100],
  "predictions": [
    { "color": "Green", "confidence": 0.952 },
    { "color": "Yellow", "confidence": 0.031 },
    { "color": "Cyan", "confidence": 0.017 }
  ]
}
```

### Model Info
```
GET /info
Response:
{
  "classes": ["Black", "Blue", "Brown", ..., "Yellow"],
  "n_neighbors": 11,
  "metric": "euclidean",
  "n_features": 3
}
```

## Troubleshooting

### Error: "Server not connected"
- Pastikan Flask server berjalan di terminal lain
- Check bahwa server listen di `http://0.0.0.0:5000`
- Cek firewall settings jika error persists

### Error: "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install flask flask-cors
```

### Webcam tidak bisa diakses
- Izinkan browser mengakses webcam saat popup muncul
- Check Windows Settings > Privacy & Security > Camera
- Pastikan no aplikasi lain using webcam

### Model tidak akurat
1. Cek pencahayaan di sekitar ROI
2. Pastikan warna yang ingin dideteksi fully di dalam ROI box
3. Jika perlu, latih ulang model dengan data baru

### CORS Error
- Flask harus di-run dengan `CORS(app)` enabled (sudah ada di code)
- Jika error persists, clear browser cache

## Performance Tips

1. **Faster Detection**
   - Webcam resolution akan auto-adjust
   - Frame rate = 30 FPS (configurable di `script.js`)

2. **Better Accuracy**
   - Gunakan pencahayaan yang stabil
   - Jangan ada shadow di ROI box
   - Positioning object jangan terlalu jauh dari camera

3. **Stability**
   - Rata-rata predictions dari multiple frames
   - Tingkatkan delay antara predictions

## File Details

### index.html
- HTML structure dengan semantic markup
- Linked ke external CSS dan JS
- Responsive design untuk mobile/tablet

### style.css
- Modern gradient backgrounds
- Flex grid layout
- Smooth animations dan transitions
- Mobile responsive dengan media queries

### script.js
- Webcam API integration
- Canvas untuk image processing
- Fetch API untuk server communication
- Real-time updates setiap frame

### app.py
- Flask server dengan CORS
- Model loading dan prediction logic
- RGB to HSV conversion
- Top-K predictions handling

## Development

### Running with Hot Reload (Recommended for Dev)
Gunakan VS Code Live Server extension:
1. Install "Live Server" extension
2. Klik kanan `index.html` -> "Open with Live Server"
3. Perubahan CSS/JS akan auto-reload

### Debug Mode
Untuk debug JavaScript:
1. Buka Browser DevTools (F12)
2. Console tab untuk error messages
3. Network tab untuk API calls

## Browser Support

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+ (dengan HTTPS)

## Known Limitations

1. Webcam hanya bisa diakses via HTTPS atau localhost
2. Single ROI box (fixed position)
3. Predictions tergantung kualitas webcam
4. Max 30 FPS untuk real-time processing

## Future Enhancements

- [ ] Multiple ROI detection
- [ ] Adjustable ROI size
- [ ] History/statistics tracking
- [ ] Export results ke CSV
- [ ] Batch image upload untuk prediction
- [ ] Model performance metrics
- [ ] Webcam calibration tool

---

**Last Updated:** 7 Desember 2025
**Version:** 1.0
**Author:** KNN Color Detection Team
