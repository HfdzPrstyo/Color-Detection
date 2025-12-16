import cv2
import joblib
import numpy as np
import os

# Get paths - models folder is at ../models
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

print("Loading model and scaler...")
print(f"Models path: {MODELS_DIR}")

# Load model dan scaler yang sudah dilatih
model_path = os.path.join(MODELS_DIR, "knn_color_model.pkl")
scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")

if not os.path.exists(model_path):
    print(f"ERROR: Model not found at {model_path}")
    print("Please run: cd training && python train.py")
    exit(1)

if not os.path.exists(scaler_path):
    print(f"ERROR: Scaler not found at {scaler_path}")
    print("Please run: cd training && python train.py")
    exit(1)

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
print("Model loaded successfully!")

# Setup webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Tidak bisa membuka webcam")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ROI position (kotak di tengah untuk ambil warna)
frame_width, frame_height = 640, 480
roi_size = 100  # ukuran kotak 100x100
roi_x = (frame_width - roi_size) // 2
roi_y = (frame_height - roi_size) // 2

# Color mapping untuk display
color_map = {
    'Red': (0, 0, 255),
    'Blue': (255, 0, 0),
    'Green': (0, 255, 0),
    'Yellow': (0, 255, 255),
    'Orange': (0, 165, 255),
    'Purple': (128, 0, 128),
    'Pink': (203, 192, 255),
    'Brown': (19, 69, 139),
    'Grey': (128, 128, 128),
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Cyan': (255, 255, 0)
}

print("Press 'q' untuk exit")
print("Mendeteksi warna dari webcam...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Tidak bisa membaca frame dari webcam")
        break
    
    # Resize frame
    frame = cv2.resize(frame, (frame_width, frame_height))
    
    # Extract ROI di tengah
    roi = frame[roi_y:roi_y+roi_size, roi_x:roi_x+roi_size]
    
    # Preprocess: ambil average RGB dari ROI
    # OpenCV reads BGR, konversi ke RGB
    b, g, r = roi.mean(axis=(0, 1))
    pixel_rgb = np.array([r, g, b], dtype=np.uint8)
    
    # Konversi RGB ke HSV untuk konsisten dengan training
    pixel_hsv = cv2.cvtColor(np.uint8([[[r, g, b]]]), cv2.COLOR_RGB2HSV)[0][0]
    
    # Scale dan predict
    pixel_scaled = scaler.transform([pixel_hsv])
    pred_label = model.predict(pixel_scaled)[0]
    probs = model.predict_proba(pixel_scaled)[0]
    confidence = max(probs) * 100
    
    # Draw ROI rectangle
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_size, roi_y+roi_size), (255, 255, 255), 2)
    
    # Draw detected color circle
    color_bgr = color_map.get(pred_label, (200, 200, 200))
    cv2.circle(frame, (roi_x + roi_size // 2, roi_y - 30), 20, color_bgr, -1)
    
    # Display result text
    text_label = f"{pred_label} ({confidence:.1f}%)"
    cv2.putText(frame, text_label, (roi_x, roi_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Display RGB values
    rgb_text = f"RGB: ({int(r)}, {int(g)}, {int(b)})"
    cv2.putText(frame, rgb_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Display HSV values
    hsv_text = f"HSV: ({int(pixel_hsv[0])}, {int(pixel_hsv[1])}, {int(pixel_hsv[2])})"
    cv2.putText(frame, hsv_text, (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Display top 3 predictions
    top_indices = np.argsort(probs)[-3:][::-1]
    top_labels = model.classes_[top_indices]
    top_probs = probs[top_indices]
    
    y_offset = frame_height - 100
    cv2.putText(frame, "Top 3 Predictions:", (10, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    for i, (label, prob) in enumerate(zip(top_labels, top_probs)):
        pred_text = f"{i+1}. {label}: {prob*100:.1f}%"
        cv2.putText(frame, pred_text, (10, y_offset + 25 + i*25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Display frame
    cv2.imshow("Color Detection - Press 'q' to exit", frame)
    
    # Check for exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Webcam ditutup")
