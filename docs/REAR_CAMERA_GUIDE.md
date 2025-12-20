# Panduan Menambahkan Fitur Kamera Belakang ke Web App

## Ringkasan
Untuk menambahkan fitur kamera belakang (rear camera) ke aplikasi web, Anda perlu memodifikasi beberapa file:
1. **index.html** - Tambah tombol untuk switch kamera
2. **script.js** - Logika untuk beralih antara kamera depan dan belakang
3. **style.css** - Styling untuk tombol switch (optional)

---

## Langkah 1: Modifikasi `templates/index.html`

### Tambahkan Tombol Switch Kamera
Tambahkan tombol di bawah tombol START/STOP CAMERA:

```html
<div class="controls">
    <button id="startBtn" class="btn-start">START CAMERA</button>
    <button id="stopBtn" class="btn-stop" disabled>STOP CAMERA</button>
    
    <!-- TAMBAH BAGIAN INI -->
    <div class="camera-switch">
        <button id="switchCameraBtn" class="btn-switch" title="Switch to rear camera">
            🔄 Switch Camera
        </button>
        <span id="cameraType" class="camera-type">Front Camera</span>
    </div>
    <!-- AKHIR TAMBAHAN -->
</div>
```

---

## Langkah 2: Modifikasi `static/script.js`

### Tambahkan Variabel State untuk Kamera
Tambahkan ini di bagian state (setelah `let selectedImage = null;`):

```javascript
// Tambahkan ini setelah let selectedImage = null;
let currentFacingMode = 'user'; // 'user' = depan, 'environment' = belakang
let currentStream = null;
```

### Modifikasi Fungsi `startCamera()`
Ubah fungsi `startCamera()` agar bisa menerima parameter `facingMode`:

```javascript
// Ganti seluruh fungsi startCamera dengan ini:
async function startCamera(facingMode = 'user') {
    try {
        // Stop kamera lama jika ada
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        const stream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: facingMode,  // Gunakan parameter facingMode
                width: 640, 
                height: 480 
            }
        });

        currentStream = stream;  // Simpan stream untuk reference nanti
        currentFacingMode = facingMode;  // Simpan facing mode yang aktif

        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            isRunning = true;
            startBtn.disabled = true;
            stopBtn.disabled = false;
            
            // Update tampilan kamera type
            const cameraTypeSpan = document.getElementById('cameraType');
            if (cameraTypeSpan) {
                cameraTypeSpan.textContent = facingMode === 'user' ? 'Front Camera' : 'Rear Camera';
            }
            
            updateStatus('active', 'Camera is running. Position object in the green box.');
            detectFrame();
        };
    } catch (error) {
        updateStatus('error', 'Error accessing camera: ' + error.message);
    }
}
```

### Modifikasi Fungsi `stopCamera()`
Update fungsi `stopCamera()` untuk menggunakan `currentStream`:

```javascript
// Ganti fungsi stopCamera dengan ini:
function stopCamera() {
    isRunning = false;
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
    }
    video.srcObject = null;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    
    // Update tampilan
    const cameraTypeSpan = document.getElementById('cameraType');
    if (cameraTypeSpan) {
        cameraTypeSpan.textContent = 'Front Camera';
    }
    
    updateStatus('inactive', 'Camera stopped');
}
```

### Tambahkan Fungsi Baru `switchCamera()`
Tambahkan fungsi baru ini (letakkan sebelum event listeners):

```javascript
// Tambahkan fungsi baru ini
function switchCamera() {
    if (!isRunning) {
        updateStatus('error', 'Please start camera first');
        return;
    }

    // Toggle antara user (depan) dan environment (belakang)
    const newFacingMode = currentFacingMode === 'user' ? 'environment' : 'user';
    
    // Mulai kamera dengan facing mode baru
    startCamera(newFacingMode);
    
    // Update status
    const message = newFacingMode === 'user' 
        ? 'Switched to Front Camera' 
        : 'Switched to Rear Camera';
    updateStatus('active', message);
}
```

### Tambahkan Event Listener untuk Tombol Switch
Temukan bagian event listeners (biasanya di akhir file) dan tambahkan:

```javascript
// Tambahkan ini di bagian event listeners
const switchCameraBtn = document.getElementById('switchCameraBtn');
if (switchCameraBtn) {
    switchCameraBtn.addEventListener('click', switchCamera);
}
```

---

## Langkah 3: Styling (Optional)

### Tambahkan CSS ke `static/style.css`

```css
/* Tambahkan ini ke style.css */
.camera-switch {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
    justify-content: center;
}

.btn-switch {
    background-color: #6c5ce7;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: background-color 0.3s ease;
}

.btn-switch:hover {
    background-color: #5f3dc4;
}

.btn-switch:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.camera-type {
    font-size: 12px;
    color: #666;
    font-weight: 500;
}
```

---

## Ringkasan Perubahan

| File | Perubahan |
|------|-----------|
| `index.html` | Tambah tombol switch kamera dan label camera type |
| `script.js` | Tambah variabel state, modifikasi `startCamera()`, `stopCamera()`, tambah `switchCamera()`, tambah event listener |
| `style.css` | Tambah styling untuk `.camera-switch` dan `.btn-switch` |

---

## Cara Kerja

1. **User memulai kamera** → Kamera depan (`user`) aktif secara default
2. **User klik "Switch Camera"** → Fungsi `switchCamera()` dipanggil
3. **Toggle facingMode** → Beralih antara `'user'` (depan) dan `'environment'` (belakang)
4. **Stream baru dibuat** → Kamera baru dimulai dengan facing mode baru
5. **UI update** → Label berubah menunjukkan kamera mana yang aktif

---

## Browser Compatibility

- ✅ Chrome/Chromium (semua versi terbaru)
- ✅ Firefox (v36+)
- ✅ Edge (semua versi terbaru)
- ✅ Safari (iOS 14.5+)
- ⚠️ Rear camera hanya tersedia di perangkat yang memiliki multiple cameras

---

## Troubleshooting

### Error: "NotAllowedError" saat switch camera
- User belum memberikan permission untuk akses kamera
- Beri permission terlebih dahulu

### Kamera belakang tidak tersedia
- Perangkat hanya memiliki 1 kamera (biasanya desktop)
- Hanya bisa digunakan di mobile/tablet dengan multiple cameras

### Masih error setelah perubahan?
- Pastikan tombol `switchCameraBtn` memiliki ID yang benar
- Check console browser untuk error messages (`F12 → Console`)
- Refresh halaman setelah membuat perubahan

---

## Bonus: Deteksi Kamera yang Tersedia (Advanced)

Jika ingin deteksi kamera apa saja yang tersedia:

```javascript
async function getAvailableCameras() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        
        console.log('Available cameras:', videoDevices.length);
        return videoDevices;
    } catch (error) {
        console.error('Error enumerating devices:', error);
        return [];
    }
}

// Gunakan saat halaman load
window.addEventListener('load', async () => {
    const cameras = await getAvailableCameras();
    // Disable switch button jika hanya 1 kamera
    const switchBtn = document.getElementById('switchCameraBtn');
    if (switchBtn && cameras.length < 2) {
        switchBtn.disabled = true;
        switchBtn.title = 'Device has only one camera';
    }
});
```

