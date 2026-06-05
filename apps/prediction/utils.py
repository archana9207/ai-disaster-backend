import joblib
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / 'ml' / 'model' / 'n_disaster_model.pkl'

# ✅ Alphabetical order from LabelEncoder: Drought, Flood, Normal, Storm
LABELS = {0: 'Drought', 1: 'Flood', 2: 'Normal', 3: 'Storm'}

model = None
explainer = None

def load_model():
    global model
    if model is None:
        try:
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Model load error: {e}")
            raise
    return model

def init_shap_explainer(background_data=None):
    global explainer
    if explainer is None and model is not None:
        try:
            import shap
            if background_data is None:
                background_data = np.random.rand(100, 5)
            explainer = shap.TreeExplainer(model, background_data)
            logger.info("SHAP explainer initialized")
        except ImportError:
            logger.warning("shap not installed")
            explainer = None
        except Exception as e:
            logger.warning(f"SHAP init failed: {e}")
            explainer = None
    return explainer

def predict_disaster(features):
    if model is None:
        load_model()
    input_array = np.array([features])
    pred_idx = model.predict(input_array)[0]
    return LABELS.get(pred_idx, 'Normal'), pred_idx

def get_shap_explanation(features, class_idx):
    if explainer is None:
        init_shap_explainer()
    if explainer is None:
        return None
    input_array = np.array([features])
    shap_values = explainer.shap_values(input_array)
    if class_idx < len(shap_values):
        vals = shap_values[class_idx][0]
        feature_names = ['Temperature', 'Humidity', 'Precipitation', 'Wind Speed', 'Pressure']
        return dict(zip(feature_names, vals.tolist()))
    return None