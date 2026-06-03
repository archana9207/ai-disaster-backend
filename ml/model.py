import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Paths
DATASET_PATH = "data/GlobalWeatherRepository.csv"   
MODEL_SAVE_PATH = "ml/model/n_disaster_model.pkl"

# 1. Load data (adjust path as needed)
df = pd.read_csv(DATASET_PATH)

# 2. Feature selection (same as in report)
df = df[['temperature_celsius', 'humidity', 'precip_mm', 'wind_kph', 'pressure_mb']].copy()

# 3. Rule‑based target variable creation
def classify_disaster(row):
    if row["precip_mm"] > 150:
        return "Flood"
    elif row["temperature_celsius"] > 35 and row["humidity"] < 30:
        return "Drought"
    elif row["wind_kph"] > 50:
        return "Storm"
    else:
        return "Normal"

df['disaster'] = df.apply(classify_disaster, axis=1)

# 4. Encode labels
le = LabelEncoder()
df['disaster_encoded'] = le.fit_transform(df['disaster'])  # order: Flood, Drought, Storm, Normal

X = df[['temperature_celsius', 'humidity', 'precip_mm', 'wind_kph', 'pressure_mb']]
y = df['disaster_encoded']

# 5. Train Random Forest (default parameters)
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# 6. Save model
joblib.dump(model, MODEL_SAVE_PATH)
print(f"Model retrained and saved to {MODEL_SAVE_PATH}")
print(f"Label mapping: {dict(enumerate(le.classes_))}")