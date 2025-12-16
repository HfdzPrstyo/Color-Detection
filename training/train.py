import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import cv2
import joblib
import os

# Get paths - models folder is at ../models
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Create directories if they don't exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Dataset path
DATASET_PATH = os.path.join(DATA_DIR, 'Warna_data.csv')

print("=" * 60)
print("TRAINING KNN COLOR MODEL")
print("=" * 60)
print(f"Dataset path: {DATASET_PATH}")
print(f"Models will be saved to: {MODELS_DIR}")

# Load dataset
if not os.path.exists(DATASET_PATH):
    print(f"ERROR: Dataset not found at {DATASET_PATH}")
    print("Please ensure Warna_data.csv is in the data/ folder")
    exit(1)

dataset = pd.read_csv(DATASET_PATH, sep=';')

# Convert RGB to HSV (lebih baik untuk warna netral seperti Grey dan Black)
print("\n1. Converting RGB to HSV...")
hsv_data = []
for idx, row in dataset.iterrows():
    rgb = np.uint8([[[row['red'], row['green'], row['blue']]]])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[0][0]
    hsv_data.append({'hue': h, 'saturation': s, 'value': v, 'label': row['label']})

dataset_hsv = pd.DataFrame(hsv_data)

# Data Cleaning: Hapus outlier (Aggressive cleaning untuk Grey & Black)
print("2. Cleaning data (Optimized)...")
print(f"   Original: {len(dataset_hsv)} samples")

# Grey yang terlalu gelap (Value < 60) atau terlalu terang (Value > 210)
grey_outliers = ((dataset_hsv['label'] == 'Grey') & ((dataset_hsv['value'] < 60) | (dataset_hsv['value'] > 210)))
# Black yang terlalu terang (Value > 50)
black_outliers = ((dataset_hsv['label'] == 'Black') & (dataset_hsv['value'] > 50))

num_grey_removed = grey_outliers.sum()
num_black_removed = black_outliers.sum()
print(f"   Removed {num_grey_removed} Grey outliers + {num_black_removed} Black outliers")

dataset_clean = dataset_hsv[~(grey_outliers | black_outliers)].copy()
print(f"   Cleaned: {len(dataset_clean)} samples")

X = dataset_clean[['hue', 'saturation', 'value']]
y = dataset_clean['label']

# Normalize features
print("\n3. Normalizing features...")
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
print("4. Train-test split...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# Train KNN model dengan parameter terbaik
print("5. Training KNN (k=11, weights=distance, metric=euclidean)...")
final_knn = KNeighborsClassifier(
    n_neighbors=11,
    weights='distance',
    metric='euclidean'
)
final_knn.fit(X_train, y_train)

# Evaluation
print("\n6. Evaluation...")
train_accuracy = final_knn.score(X_train, y_train)
test_accuracy = final_knn.score(X_test, y_test)
print(f"   Train Accuracy: {train_accuracy:.4f}")
print(f"   Test Accuracy:  {test_accuracy:.4f}")

# Get predictions
y_pred = final_knn.predict(X_test)

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)
print(classification_report(y_test, y_pred))

# Save model & scaler
print("\n7. Saving model...")
model_path = os.path.join(MODELS_DIR, "knn_color_model.pkl")
scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")

joblib.dump(final_knn, model_path)
joblib.dump(scaler, scaler_path)
print(f"   Model saved to: {model_path}")
print(f"   Scaler saved to: {scaler_path}")
print("\n   Model and scaler saved successfully!")
