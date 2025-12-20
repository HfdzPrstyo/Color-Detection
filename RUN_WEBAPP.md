# 🚀 Cara Menjalankan Web App dengan Fitur Kamera Belakang

## 📋 Prerequisites (Persiapan)

Pastikan Anda sudah memiliki:
- Python 3.7+ terinstall
- Folder `models/` berisi file:
  - `knn_color_model.pkl`
  - `scaler.pkl`

Jika belum punya model, train terlebih dahulu:
```bash
cd training
python train.py
cd ..
```

---

## ⚙️ Langkah 1: Install Dependencies

Buka terminal/PowerShell di folder project (`d:\Kuliah\Semester 5\coba`):

```bash
pip install -r requirements.txt
```

**Jika error, coba install manual:**
```bash
pip install flask flask-cors pillow opencv-python joblib numpy scikit-learn
```

---

## ▶️ Langkah 2: Jalankan Flask Server

Di terminal yang sama, jalankan:

```bash
python app.py
```

Anda akan melihat output seperti ini:
```
Loading model and scaler...
Base directory: d:\Kuliah\Semester 5\coba
Models path: d:\Kuliah\Semester 5\coba\models
Model path: d:\Kuliah\Semester 5\coba\models\knn_color_model.pkl
Scaler path: d:\Kuliah\Semester 5\coba\models\scaler.pkl
Model loaded successfully!
 * Running on http://127.0.0.1:5000
```

⚠️ **Jangan tutup terminal ini! Biarkan Flask server tetap berjalan.**

---

## 🌐 Langkah 3: Buka Browser

Buka browser (Chrome, Firefox, Edge, Safari) dan pergi ke:

```
http://localhost:5000
```

atau

```
http://127.0.0.1:5000
```

---

## 📱 Langkah 4: Gunakan Fitur Kamera Belakang

### Saat di halaman web:

1. **Klik "START CAMERA"** 
   - Kamera depan akan menyala
   - Lihat label "Front Camera" di bawah tombol

2. **Klik "🔄 Switch Camera"**
   - Akan beralih ke kamera belakang
   - Label berubah menjadi "Rear Camera"

3. **Klik lagi "🔄 Switch Camera"**
   - Kembali ke kamera depan

4. **Klik "STOP CAMERA"**
   - Matikan kamera

---

## ✨ Fitur yang Sudah Diimplementasikan

- ✅ Tombol "Switch Camera" untuk beralih antara kamera depan/belakang
- ✅ Label yang menunjukkan kamera mana yang aktif
- ✅ Deteksi warna real-time dengan kamera depan atau belakang
- ✅ Upload gambar untuk deteksi warna
- ✅ Prediksi top 3 warna
- ✅ Tampilan RGB & HSV values

---

## 🐛 Troubleshooting

### Browser meminta permission kamera
**Solusi:** Klik "Allow" untuk memberikan akses kamera

### Error: "Server not connected"
**Solusi:** 
- Pastikan Flask server masih berjalan di terminal
- Refresh halaman browser (Ctrl+F5)
- Cek apakah port 5000 tidak terpakai

### Kamera belakang tidak tersedia
**Penyebab:** Device hanya memiliki 1 kamera (desktop)
**Solusi:** Fitur ini hanya bekerja di perangkat dengan multiple cameras (smartphone, tablet)

### Model tidak ditemukan
**Error:** "Model not found at..."
**Solusi:**
```bash
# Jalankan training terlebih dahulu
cd training
python train.py
# Kembali ke folder utama
cd ..
# Jalankan app.py lagi
python app.py
```

### Camera error: "NotAllowedError"
**Penyebab:** Permission ditolak
**Solusi:** 
- Refresh halaman dan klik "Allow"
- Cek setting kamera di browser

---

## 📁 File Structure

```
coba/
├── app.py                  # Flask server (JALANKAN INI)
├── requirements.txt        # Dependencies
├── templates/
│   └── index.html         # Halaman web (sudah update)
├── static/
│   ├── script.js          # JavaScript (sudah update dengan fitur switch camera)
│   └── style.css          # CSS styling (sudah update)
├── models/
│   ├── knn_color_model.pkl
│   └── scaler.pkl
└── training/
    ├── train.py
    └── requirements.txt
```

---

## 🎯 Ringkasan Perubahan

| File | Perubahan |
|------|-----------|
| `script.js` | Tambah logika switch kamera, variabel state |
| `index.html` | Tambah tombol switch kamera & label |
| `style.css` | Tambah styling untuk tombol & label |

---

## 💡 Tips

1. **Untuk performa lebih baik**: Tempatkan object dengan pencahayaan yang cukup di area ROI (kotak hijau)
2. **Ubah FRAME_INTERVAL_MS**: Di script.js baris 3, ubah nilai untuk mengubah kecepatan deteksi
3. **Kamera belakang untuk testing lingkungan**: Gunakan kamera belakang untuk mendeteksi warna dari sudut berbeda

---

## ❓ Pertanyaan Umum

**Q: Berapa kecepatan deteksi?**
A: Default 3 detik (3000ms). Ubah `FRAME_INTERVAL_MS` di script.js untuk mengubahnya.

**Q: Bisa gunakan kamera eksternal?**
A: Ya, browser akan menggunakan device video input yang tersedia.

**Q: Model mana yang digunakan?**
A: KNN (k-Nearest Neighbors) dengan HSV color space.

---

## ✅ Testing Checklist

- [ ] Flask server berjalan tanpa error
- [ ] Browser bisa akses http://localhost:5000
- [ ] Tombol "START CAMERA" berfungsi
- [ ] Label menunjukkan "Front Camera"
- [ ] Kamera depan menampilkan video
- [ ] Tombol "Switch Camera" berfungsi
- [ ] Dapat beralih ke kamera belakang (jika tersedia)
- [ ] Deteksi warna berfungsi
- [ ] Label di bawah tombol update sesuai kamera aktif

---

**Selamat! Web app Anda siap digunakan dengan fitur kamera belakang 🎉**
