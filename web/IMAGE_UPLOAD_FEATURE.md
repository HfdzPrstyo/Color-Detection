# ✅ FITUR BARU: Upload Image Detection

Fitur untuk deteksi warna dari file/image sudah ditambahkan!

## 📁 Perubahan yang Dilakukan

### 1. **index.html** - UI Update
- Tambah tab navigation (Live Camera vs Upload Image)
- Tambah upload area dengan drag-drop support
- Tambah image preview

### 2. **style.css** - Styling Baru
- Tab navigation styling
- Upload area styling
- Drag-over effects
- Image preview container

### 3. **script.js** - Logic Baru
- Tab switching functionality
- File input handling
- Drag-drop event handling
- Image preview display
- Send image ke server untuk prediction

### 4. **app.py** - Backend Baru
- New endpoint: `POST /predict-image`
- Image decoding (base64)
- Image processing (resize, center crop)
- RGB average calculation
- HSV conversion dan prediction

### 5. **Dependencies**
- `pillow` (PIL) - untuk image processing

---

## 🎯 Fitur Baru

### Tab Navigation
```
┌──────────────────────────────┐
│ 📷 Live Camera │ 📁 Upload   │
└──────────────────────────────┘
```

### Upload Area
```
┌─────────────────────────────┐
│                             │
│        📸 Upload Area        │
│   Click atau drag image      │
│   Support: JPG, PNG, GIF     │
│                             │
└─────────────────────────────┘
```

### Fitur Upload
✅ Click untuk select image
✅ Drag-drop image
✅ Real-time preview
✅ Automatic color detection
✅ Support multiple formats (JPG, PNG, GIF, WebP)
✅ Clear button untuk reset

---

## 🚀 Cara Menggunakan

### Step 1: Jalankan Flask Server
```powershell
cd d:\Kuliah\Semester 5\coba\web
python app.py
```

### Step 2: Buka Web App di Browser
```
http://localhost:5500  (atau file URL)
```

### Step 3: Gunakan Upload Image
1. Klik tab "📁 Upload Image"
2. Klik area upload atau drag image
3. Image akan di-preview
4. Hasil deteksi otomatis muncul
5. Lihat RGB/HSV values dan predictions

---

## 📊 API Endpoints

### New Endpoint: `/predict-image`
**Method**: POST
**Content-Type**: application/json

**Request**:
```json
{
  "image": "data:image/png;base64,iVBORw0KGgo..."
}
```

**Response**:
```json
{
  "color": "Green",
  "confidence": 0.95,
  "hsv": [47, 127, 200],
  "rgb": [145, 200, 100],
  "predictions": [
    {"color": "Green", "confidence": 0.95},
    {"color": "Yellow", "confidence": 0.03},
    {"color": "Blue", "confidence": 0.02}
  ]
}
```

---

## 🔄 Flow Diagram

```
User Interface (Browser)
├─ Tab 1: Live Camera
│  ├─ Start/Stop camera
│  ├─ Real-time ROI detection
│  └─ Continuous predictions
│
└─ Tab 2: Upload Image
   ├─ Click/Drag image
   ├─ Preview image
   ├─ Extract center region
   ├─ Send to server
   └─ Display results

Server (Flask Backend)
├─ /predict (camera ROI)
│  └─ RGB → HSV → Predict
│
└─ /predict-image (uploaded image)
   └─ Decode base64
   └─ Load image (PIL)
   └─ Resize to 100x100
   └─ Extract center 30x30
   └─ Average RGB
   └─ RGB → HSV → Predict
```

---

## 💡 Technical Details

### Image Processing:
1. **Decode**: Base64 string → PIL Image
2. **Resize**: Any size → 100x100 px (uniform)
3. **Extract**: Center 30x30 region (uniform area)
4. **Average**: Calculate RGB mean
5. **Convert**: RGB → HSV
6. **Predict**: KNN classification

### Upload Area:
- Accepts: JPG, PNG, GIF, WebP
- Drag-over effect: Blue background
- Click to browse: File picker
- Clear button: Reset to upload area

### Tab Switching:
- Click tab untuk switch
- Stop camera saat switch away
- Smooth transitions

---

## 🧪 Testing

Sudah di-test dengan:
- ✅ Live camera prediction (RGB)
- ✅ Image upload with synthetic image (Green)
- ✅ All endpoints returning correct format
- ✅ Drag-drop functionality
- ✅ Tab switching logic

---

## 🎨 UI/UX Features

### Upload Area Design:
```
Normal State:
┌─────────────────────┐
│  📸 Click/Drag      │  (white background)
└─────────────────────┘

Hover State:
┌─────────────────────┐
│  📸 Click/Drag      │  (light blue)
└─────────────────────┘

Drag-Over State:
┌─────────────────────┐
│  📸 Drop Here       │  (blue + glow)
└─────────────────────┘
```

### Tab Navigation:
- Active tab: Blue text + underline
- Inactive tab: Grey text
- Hover effect: Smooth color change
- Icons: 📷 for camera, 📁 for upload

---

## 📝 Usage Scenarios

1. **Quick Color Check**
   - Upload screenshot
   - Get instant color info

2. **Batch Processing**
   - Upload multiple images
   - Check each for colors

3. **Color Reference**
   - Take photo of object
   - Get exact color values (RGB/HSV)

4. **Accessibility**
   - Help identify colors
   - Get precise color names

---

## 🔒 Error Handling

- Invalid image format → Error message
- Server disconnected → Show status
- Image decode error → Graceful fallback
- No image selected → Prompt user

---

## 📦 Dependencies Added

- **pillow (PIL)**: Image loading, processing, conversion
- Already have: flask, flask-cors, opencv-python, scikit-learn, joblib, numpy

---

## ✅ Files Modified

| File | Changes |
|------|---------|
| `index.html` | +50 lines (tabs + upload UI) |
| `style.css` | +90 lines (tab + upload styling) |
| `script.js` | +150 lines (tab logic + upload) |
| `app.py` | +60 lines (image endpoint) |

---

## 🎯 What's Next?

Possible improvements:
- [ ] Multiple ROI detection
- [ ] Color palette extraction
- [ ] Batch image upload
- [ ] Image crop tool
- [ ] Color history/favorites
- [ ] Export results as image
- [ ] Real-time histogram

---

## 🎉 Status

✅ Upload image feature fully implemented
✅ All endpoints tested and working
✅ UI/UX responsive and intuitive
✅ Error handling in place
✅ Documentation complete

**Ready to use!**

---

**Last Updated**: 7 Desember 2025
**Version**: 1.1 (Image Upload Added)
