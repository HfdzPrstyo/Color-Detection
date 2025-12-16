// Configuration
const API_URL = 'http://localhost:5000';
const ROI_SIZE = 120;
// Interval between detections in milliseconds. Set to ~3000ms for ~3 seconds.
const FRAME_INTERVAL_MS = 3000;

// DOM Elements - Camera
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const status = document.getElementById('status');
const apiStatus = document.getElementById('apiStatus');

// DOM Elements - Upload
const imageInput = document.getElementById('imageInput');
const uploadArea = document.getElementById('uploadArea');
const uploadedImage = document.getElementById('uploadedImage');
const previewImage = document.getElementById('previewImage');
const selectImageBtn = document.getElementById('selectImageBtn');
const clearImageBtn = document.getElementById('clearImageBtn');
const uploadStatus = document.getElementById('uploadStatus');

// DOM Elements - Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// State
let isRunning = false;
let apiConnected = false;
let selectedImage = null;

// Color names to RGB mapping for preview
const colorRGBMap = {
    'Red': [255, 0, 0],
    'Blue': [0, 0, 255],
    'Green': [0, 255, 0],
    'Yellow': [255, 255, 0],
    'Orange': [255, 165, 0],
    'Purple': [128, 0, 128],
    'Pink': [255, 192, 203],
    'Brown': [139, 69, 19],
    'Grey': [128, 128, 128],
    'Black': [0, 0, 0],
    'White': [255, 255, 255],
    'Cyan': [0, 255, 255]
};

// Check API connection
async function checkAPI() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            apiConnected = true;
            apiStatus.className = 'api-status connected';
            apiStatus.textContent = '✓ Connected to server';
            return true;
        }
    } catch (error) {
        apiConnected = false;
        apiStatus.className = 'api-status error';
        apiStatus.textContent = '✗ Server not connected. Make sure Flask server is running.';
        return false;
    }
}

// Start camera
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user', width: 640, height: 480 }
        });

        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            isRunning = true;
            startBtn.disabled = true;
            stopBtn.disabled = false;
            updateStatus('active', 'Camera is running. Position object in the green box.');
            detectFrame();
        };
    } catch (error) {
        updateStatus('error', 'Error accessing camera: ' + error.message);
    }
}

// Stop camera
function stopCamera() {
    isRunning = false;
    const stream = video.srcObject;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    video.srcObject = null;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    updateStatus('', 'Camera stopped.');
    clearResults();
}

// Update status message
function updateStatus(type, message) {
    if (type) {
        status.className = `status ${type}`;
        status.innerHTML = message;
    } else {
        status.className = 'status';
    }
}

// Clear results
function clearResults() {
    document.getElementById('colorName').textContent = '-';
    document.getElementById('confidencePercent').textContent = '0%';
    document.getElementById('confidenceFill').style.width = '0%';
    document.getElementById('valueR').textContent = '0';
    document.getElementById('valueG').textContent = '0';
    document.getElementById('valueB').textContent = '0';
    document.getElementById('valueH').textContent = '0';
    document.getElementById('valueS').textContent = '0';
    document.getElementById('valueV').textContent = '0';
    document.getElementById('roiColor').style.background = 'rgb(128, 128, 128)';
    document.getElementById('predictedColor').style.background = 'rgb(128, 128, 128)';
    document.getElementById('predictionsList').innerHTML = '<div style="color: #999; text-align: center; padding: 20px;">Waiting for predictions...</div>';
}

// Detect frame
function detectFrame() {
    if (!isRunning) return;

    // Draw current frame to canvas
    ctx.save();
    ctx.scale(-1, 1);
    ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
    ctx.restore();

    // Extract ROI (center of canvas)
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const roiX = centerX - ROI_SIZE / 2;
    const roiY = centerY - ROI_SIZE / 2;

    const imageData = ctx.getImageData(roiX, roiY, ROI_SIZE, ROI_SIZE);
    const data = imageData.data;

    // Calculate average RGB
    let r = 0, g = 0, b = 0;
    for (let i = 0; i < data.length; i += 4) {
        r += data[i];
        g += data[i + 1];
        b += data[i + 2];
    }
    const pixelCount = data.length / 4;
    r = Math.round(r / pixelCount);
    g = Math.round(g / pixelCount);
    b = Math.round(b / pixelCount);

    // Send to API for prediction
    if (apiConnected) {
        sendPrediction(r, g, b);
    }

    // Schedule next frame (delay between detections)
    setTimeout(detectFrame, FRAME_INTERVAL_MS);
}

// Send prediction request
async function sendPrediction(r, g, b) {
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ r, g, b })
        });

        if (response.ok) {
            const result = await response.json();
            displayResults(result, r, g, b);
        }
    } catch (error) {
        console.error('Prediction error:', error);
    }
}

// Display results
function displayResults(result, r, g, b) {
    // Main result
    document.getElementById('colorName').textContent = result.color;
    const confidence = result.confidence * 100;
    document.getElementById('confidencePercent').textContent = confidence.toFixed(1) + '%';
    document.getElementById('confidenceFill').style.width = (confidence) + '%';

    // RGB values
    document.getElementById('valueR').textContent = r;
    document.getElementById('valueG').textContent = g;
    document.getElementById('valueB').textContent = b;

    // HSV values
    document.getElementById('valueH').textContent = result.hsv[0];
    document.getElementById('valueS').textContent = result.hsv[1];
    document.getElementById('valueV').textContent = result.hsv[2];

    // Color preview
    document.getElementById('roiColor').style.background = `rgb(${r}, ${g}, ${b})`;
    const rgb = colorRGBMap[result.color] || [128, 128, 128];
    document.getElementById('predictedColor').style.background = `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;

    // Top predictions
    displayPredictions(result.predictions);
}

// Display top predictions
function displayPredictions(predictions) {
    const list = document.getElementById('predictionsList');
    list.innerHTML = '';

    predictions.forEach((pred, index) => {
        const percent = (pred.confidence * 100).toFixed(1);
        const item = document.createElement('div');
        item.className = 'prediction-item';
        item.innerHTML = `
            <span class="prediction-name">${index + 1}. ${pred.color}</span>
            <div class="prediction-bar">
                <div class="prediction-fill" style="width: ${percent}%"></div>
            </div>
            <span class="prediction-percent">${percent}%</span>
        `;
        list.appendChild(item);
    });
}

// TAB SWITCHING
function switchTab(tabName) {
    // Hide all tabs
    tabContents.forEach(tab => tab.classList.remove('active'));
    // Deactivate all buttons
    tabBtns.forEach(btn => btn.classList.remove('active'));
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    // Activate button
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Stop camera if switching away
    if (tabName !== 'camera' && isRunning) {
        stopCamera();
    }
}

// UPLOAD FUNCTIONALITY
selectImageBtn.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', (e) => {
    handleImageSelect(e.target.files[0]);
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleImageSelect(e.dataTransfer.files[0]);
});

uploadArea.addEventListener('click', () => {
    imageInput.click();
});

clearImageBtn.addEventListener('click', () => {
    selectedImage = null;
    imageInput.value = '';
    uploadArea.style.display = 'flex';
    uploadedImage.style.display = 'none';
    clearImageBtn.disabled = true;
    clearResults();
});

function handleImageSelect(file) {
    if (!file || !file.type.startsWith('image/')) {
        updateUploadStatus('error', 'Please select a valid image file');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        uploadedImage.style.display = 'flex';
        clearImageBtn.disabled = false;
        selectedImage = e.target.result;
        
        updateUploadStatus('loading', 'Analyzing image...');
        
        // Send image to server for detection
        sendImagePrediction(e.target.result);
    };
    reader.readAsDataURL(file);
}

function updateUploadStatus(type, message) {
    if (type) {
        uploadStatus.className = `status ${type}`;
        uploadStatus.innerHTML = message;
    } else {
        uploadStatus.className = 'status';
    }
}

function sendImagePrediction(imageData) {
    if (!apiConnected) {
        updateUploadStatus('error', 'Server not connected');
        return;
    }

    fetch(`${API_URL}/predict-image`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            updateUploadStatus('error', 'Error: ' + result.error);
        } else {
            displayResults(result, result.rgb[0], result.rgb[1], result.rgb[2]);
            updateUploadStatus('', '');
        }
    })
    .catch(error => {
        console.error('Upload prediction error:', error);
        updateUploadStatus('error', 'Error analyzing image');
    });
}

// Tab button listeners
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        switchTab(btn.dataset.tab);
    });
});

// Event listeners
startBtn.addEventListener('click', startCamera);
stopBtn.addEventListener('click', stopCamera);

// Initialize
window.addEventListener('load', () => {
    checkAPI();
    setInterval(checkAPI, 5000);
});
