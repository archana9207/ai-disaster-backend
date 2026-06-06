import joblib
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / 'ml' / 'model' / 'n_disaster_model.pkl'

# Updated for 5 classes: index → name
# From retraining script: Cyclone=0, Drought=1, Flood=2, Normal=3, Storm=4
LABELS = {0: 'Cyclone', 1: 'Drought', 2: 'Flood', 3: 'Normal', 4: 'Storm'}

model = None
explainer = None

def load_model():
    global model
    if model is None:
        try:
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded from %s", MODEL_PATH)
            logger.info("Using label map: %s", LABELS)
        except Exception as e:
            logger.error("Failed to load model: %s", e)
            raise
    return model

def init_shap_explainer(background_data=None):
    global explainer
    if explainer is None and model is not None:
        try:
            import shap
            if background_data is None:
                rng = np.random.default_rng(42)
                background_data = np.column_stack([
                    rng.uniform(-10, 50, 100),
                    rng.uniform(0, 100, 100),
                    rng.uniform(0, 300, 100),
                    rng.uniform(0, 150, 100),
                    rng.uniform(950, 1050, 100),
                ])
            explainer = shap.TreeExplainer(model, background_data)
            logger.info("SHAP explainer initialised")
        except ImportError:
            logger.warning("shap not installed")
            explainer = None
        except Exception as e:
            logger.warning("SHAP init failed: %s", e)
            explainer = None
    return explainer

def predict_disaster(features):
    if model is None:
        load_model()
    input_array = np.array([features], dtype=float)
    pred_idx = int(model.predict(input_array)[0])
    label = LABELS.get(pred_idx, 'Normal')
    return label, pred_idx

def get_shap_explanation(features, class_idx):
    if explainer is None:
        init_shap_explainer()
    if explainer is None:
        return None
    try:
        input_array = np.array([features], dtype=float)
        shap_values = explainer.shap_values(input_array)
        feature_names = ['Temperature', 'Humidity', 'Precipitation', 'Wind Speed', 'Pressure']
        if isinstance(shap_values, list):
            vals = shap_values[class_idx][0] if class_idx < len(shap_values) else shap_values[0][0]
        else:
            vals = shap_values[0, :, class_idx] if shap_values.ndim == 3 else shap_values[0]
        return dict(zip(feature_names, [float(v) for v in vals]))
    except Exception as e:
        logger.warning("SHAP computation failed: %s", e)
        return None