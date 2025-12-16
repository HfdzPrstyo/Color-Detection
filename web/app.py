from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import cv2
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Get paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load model dan scaler dari models folder
print("Loading model and scaler...")
print(f"Base directory: {BASE_DIR}")
print(f"Models path: {MODELS_DIR}")
try:
    model_path = os.path.join(MODELS_DIR, "knn_color_model.pkl")
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    
    print(f"Model path: {model_path}")
    print(f"Scaler path: {scaler_path}")
    
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found at {model_path}")
    if not os.path.exists(scaler_path):
        print(f"ERROR: Scaler file not found at {scaler_path}")
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = None

# Serve main page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    if model is not None and scaler is not None:
        return jsonify({'status': 'ok', 'model': 'loaded'}), 200
    else:
        return jsonify({'status': 'error', 'model': 'not_loaded'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Predict color from RGB values"""
    try:
        data = request.get_json()
        r = data.get('r', 128)
        g = data.get('g', 128)
        b = data.get('b', 128)

        # Convert RGB to HSV
        rgb = np.uint8([[[r, g, b]]])
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0][0]
        h, s, v = int(hsv[0]), int(hsv[1]), int(hsv[2])

        # Scale and predict
        hsv_array = np.array([[h, s, v]])
        hsv_scaled = scaler.transform(hsv_array)
        
        prediction = model.predict(hsv_scaled)[0]
        probabilities = model.predict_proba(hsv_scaled)[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = [
            {
                'color': model.classes_[idx],
                'confidence': float(probabilities[idx])
            }
            for idx in top_indices
        ]
        
        return jsonify({
            'color': prediction,
            'confidence': float(max(probabilities)),
            'hsv': [h, s, v],
            'rgb': [r, g, b],
            'predictions': top_predictions
        }), 200

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/predict-image', methods=['POST'])
def predict_image():
    """Predict color from uploaded image"""
    try:
        import base64
        from io import BytesIO
        from PIL import Image
        
        data = request.get_json()
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Resize untuk uniform processing
        image = image.resize((100, 100))
        
        # Convert ke RGB jika perlu
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL Image ke numpy array (RGB)
        img_array = np.array(image)
        
        # Calculate average RGB from center region
        h, w = img_array.shape[:2]
        center_size = 30
        center_y = (h - center_size) // 2
        center_x = (w - center_size) // 2
        
        center_region = img_array[center_y:center_y+center_size, center_x:center_x+center_size]
        avg_rgb = center_region.mean(axis=(0, 1)).astype(int)
        r, g, b = avg_rgb[0], avg_rgb[1], avg_rgb[2]
        
        # Convert RGB to HSV
        rgb = np.uint8([[[r, g, b]]])
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0][0]
        h_val, s_val, v_val = int(hsv[0]), int(hsv[1]), int(hsv[2])
        
        # Scale and predict
        hsv_array = np.array([[h_val, s_val, v_val]])
        hsv_scaled = scaler.transform(hsv_array)
        
        prediction = model.predict(hsv_scaled)[0]
        probabilities = model.predict_proba(hsv_scaled)[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = [
            {
                'color': model.classes_[idx],
                'confidence': float(probabilities[idx])
            }
            for idx in top_indices
        ]
        
        return jsonify({
            'color': prediction,
            'confidence': float(max(probabilities)),
            'hsv': [h_val, s_val, v_val],
            'rgb': [int(r), int(g), int(b)],
            'predictions': top_predictions
        }), 200

    except Exception as e:
        print(f"Image prediction error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'classes': list(model.classes_),
        'n_neighbors': model.n_neighbors,
        'metric': model.metric,
        'n_features': model.n_features_in_
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
