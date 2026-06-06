import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

print("Generating CLEAN, NON-OVERLAPPING dataset...")
np.random.seed(42)
n_per_class = 3000  # plenty of samples

def generate_samples(disaster_type, n):
    if disaster_type == 'Flood':
        # Flood: precip > 150, wind <= 50 (NO high wind)
        temp = np.random.uniform(-10, 50, n)
        hum = np.random.uniform(0, 100, n)
        precip = np.random.uniform(151, 300, n)
        wind = np.random.uniform(0, 50, n)          # <=50 to avoid storm overlap
        pressure = np.random.uniform(970, 1050, n)
    elif disaster_type == 'Storm':
        # Storm: wind > 50, precip <= 150 (NO extreme rain)
        temp = np.random.uniform(-10, 50, n)
        hum = np.random.uniform(0, 100, n)
        precip = np.random.uniform(0, 150, n)       # <=150 to avoid flood overlap
        wind = np.random.uniform(50.1, 120, n)
        pressure = np.random.uniform(970, 1050, n)
    elif disaster_type == 'Cyclone':
        # Cyclone: very high wind + heavy rain + low pressure
        temp = np.random.uniform(20, 35, n)
        hum = np.random.uniform(70, 100, n)
        precip = np.random.uniform(100, 300, n)
        wind = np.random.uniform(90, 180, n)
        pressure = np.random.uniform(940, 990, n)
    elif disaster_type == 'Drought':
        temp = np.random.uniform(35.1, 50, n)
        hum = np.random.uniform(0, 29.9, n)
        precip = np.random.uniform(0, 50, n)
        wind = np.random.uniform(0, 80, n)
        pressure = np.random.uniform(980, 1050, n)
    else:  # Normal
        temp = np.random.uniform(-10, 35, n)
        hum = np.random.uniform(30, 100, n)
        precip = np.random.uniform(0, 150, n)
        wind = np.random.uniform(0, 50, n)
        pressure = np.random.uniform(1000, 1050, n)
    return np.column_stack([temp, hum, precip, wind, pressure]), [disaster_type] * n

# Build dataset
X_list = []
y_list = []
for disaster in ['Flood', 'Storm', 'Cyclone', 'Drought', 'Normal']:
    X_part, y_part = generate_samples(disaster, n_per_class)
    X_list.append(X_part)
    y_list.extend(y_part)

X = np.vstack(X_list)
le = LabelEncoder()
y = le.fit_transform(y_list)

print("Label mapping (alphabetical):", dict(zip(le.classes_, le.transform(le.classes_))))
# Alphabetical order: Cyclone, Drought, Flood, Normal, Storm
# Indices: 0=Cyclone, 1=Drought, 2=Flood, 3=Normal, 4=Storm

model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1)
model.fit(X, y)

os.makedirs('ml/model', exist_ok=True)
joblib.dump(model, 'ml/model/n_disaster_model.pkl')
print("Model saved to ml/model/n_disaster_model.pkl")

# Verify
test_cases = [
    ([25, 60, 160, 20, 1013], 'Flood'),
    ([25, 60, 50, 60, 1013], 'Storm'),
    ([28, 85, 150, 120, 970], 'Cyclone'),
    ([38, 20, 10, 20, 1013], 'Drought'),
    ([20, 60, 20, 20, 1020], 'Normal'),
]
print("\nVerification:")
for features, expected in test_cases:
    pred_idx = model.predict([features])[0]
    pred_label = le.inverse_transform([pred_idx])[0]
    print(f"Expected: {expected:8} | Got: {pred_label:8} | {'✓' if pred_label == expected else '✗'}")