import joblib
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Path to the trained model
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / 'ml' / 'model' / 'n_disaster_model.pkl'

# Label mapping (must match the order used during training)
# Training code used LabelEncoder; we reconstruct order from report: 
# Flood, Drought, Storm, Normal → encoded as 0,1,2,3
LABELS = {0: 'Flood', 1: 'Drought', 2: 'Storm', 3: 'Normal'}

# Global variables (loaded once at server startup)
model = None
explainer = None


def load_model():
    """Load the Random Forest model from disk."""
    global model
    if model is None:
        try:
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully from %s", MODEL_PATH)
        except Exception as e:
            logger.error("Failed to load model: %s", e)
            raise
    return model


def init_shap_explainer(background_data: np.ndarray = None):
    """
    Initialize the SHAP TreeExplainer for the Random Forest model.
    background_data: Optional sample data (numpy array of shape [n_samples, 5]).
    If not provided, a random background is generated (not ideal but prevents crashes).
    """
    global explainer
    if explainer is None and model is not None:
        try:
            import shap
            if background_data is None:
                # Fallback: generate random background (5 features)
                background_data = np.random.rand(100, 5)
            explainer = shap.TreeExplainer(model, background_data)
            logger.info("SHAP explainer initialized")
        except ImportError:
            logger.warning("shap library not installed. SHAP explanations disabled.")
            explainer = None
        except Exception as e:
            logger.warning("Could not initialize SHAP explainer: %s", e)
            explainer = None
    return explainer


def predict_disaster(features: list) -> tuple:
    """
    Predict disaster type from a list of 5 features.
    Returns (predicted_label, class_index)
    """
    if model is None:
        load_model()
    input_array = np.array([features])
    pred_idx = model.predict(input_array)[0]
    return LABELS.get(pred_idx, 'Normal'), pred_idx


def get_shap_explanation(features: list, class_idx: int):
    """
    Compute SHAP values for the prediction.
    Returns a dictionary of feature -> importance value for the predicted class.
    """
    if explainer is None:
        init_shap_explainer()
    if explainer is None:
        return None
    
    input_array = np.array([features])
    shap_values = explainer.shap_values(input_array)
    # shap_values is a list: one array per class
    if class_idx < len(shap_values):
        shap_vals_for_class = shap_values[class_idx][0]  # first (only) row
        feature_names = ['Temperature', 'Humidity', 'Precipitation', 'Wind Speed', 'Pressure']
        return dict(zip(feature_names, shap_vals_for_class.tolist()))
    return None