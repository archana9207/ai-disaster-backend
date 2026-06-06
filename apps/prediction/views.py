import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import PredictionHistory
from .serializers import WeatherInputSerializer, PredictionResponseSerializer
from .decision_support import get_decision_support
from .utils import get_shap_explanation, load_model, init_shap_explainer

logger = logging.getLogger(__name__)

# Load model only for SHAP (not for classification)
load_model()
init_shap_explainer()

def classify_by_rules(temp, humidity, precip, wind, pressure):
    """
    Rule-based classification – 100% deterministic.
    Returns (disaster_type, class_index)
    """
    # Ensure all values are numeric (convert if needed)
    try:
        temp = float(temp)
        humidity = float(humidity)
        precip = float(precip)
        wind = float(wind)
        pressure = float(pressure)
    except (ValueError, TypeError) as e:
        print(f"⚠️ Conversion error: {e}")
        return 'Normal', 3  # fallback

    # Debug print
    print(f"🔍 Rules: precip={precip}, wind={wind}, pressure={pressure}, temp={temp}, humidity={humidity}")

    # Priority order (first match wins)
    # Cyclone: extreme wind + heavy rain + low pressure
    if wind > 80 and precip > 100 and pressure < 990:
        print("✅ Cyclone triggered")
        return 'Cyclone', 0
    # Flood: heavy rain (must be checked before Storm because storm also has high wind but with less rain)
    elif precip > 150:
        print("✅ Flood triggered")
        return 'Flood', 2
    # Storm: high wind (but not enough rain to be flood)
    elif wind > 50:
        print("✅ Storm triggered")
        return 'Storm', 4
    # Drought: high temperature and low humidity
    elif temp > 35 and humidity < 30:
        print("✅ Drought triggered")
        return 'Drought', 1
    else:
        print("✅ Normal triggered")
        return 'Normal', 3


class PredictDisasterView(APIView):
    """
    POST /api/predict/
    Uses rule-based classification (deterministic). SHAP from model if available.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Log received data for debugging
        print("📥 Received request data:", request.data)

        serializer = WeatherInputSerializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Serializer errors:", serializer.errors)
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract validated data
        temp = serializer.validated_data['temperature_celsius']
        humidity = serializer.validated_data['humidity']
        precip = serializer.validated_data['precip_mm']
        wind = serializer.validated_data['wind_kph']
        pressure = serializer.validated_data['pressure_mb']
        features = [temp, humidity, precip, wind, pressure]

        # Rule-based classification
        disaster_type, class_idx = classify_by_rules(temp, humidity, precip, wind, pressure)
        print(f"✅ Classification result: {disaster_type} (index {class_idx})")

        # Decision support recommendations
        support = get_decision_support(disaster_type)

        # SHAP explanation (optional, from ML model using the same class index)
        shap_explanation = None
        try:
            shap_explanation = get_shap_explanation(features, class_idx)
        except Exception as e:
            logger.warning(f"SHAP explanation failed: {e}")

        # Save prediction history
        try:
            PredictionHistory.objects.create(
                user=request.user,
                temperature=temp,
                humidity=humidity,
                precip_mm=precip,
                wind_kph=wind,
                pressure_mb=pressure,
                predicted_disaster=disaster_type
            )
        except Exception as e:
            logger.warning(f"Failed to save history: {e}")

        # Build response
        response_data = {
            "disaster_type": disaster_type,
            "recommendation": support["recommendation"],
            "actions": support["actions"],
            "shap_explanation": shap_explanation,
            "message": f"Rule-based assessment: {disaster_type} risk detected."
        }

        response_serializer = PredictionResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)