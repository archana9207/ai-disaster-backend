import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import PredictionHistory
from .serializers import WeatherInputSerializer, PredictionResponseSerializer
from .decision_support import get_decision_support
from .utils import predict_disaster, get_shap_explanation, load_model, init_shap_explainer

logger = logging.getLogger(__name__)

# Load model and SHAP explainer once when the module is loaded
load_model()
init_shap_explainer()  # will create random background if needed


class PredictDisasterView(APIView):
    """
    POST /api/predict/
    Accepts weather data, returns disaster type, decision support, and SHAP explanation.
    Requires JWT authentication (user must be logged in).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WeatherInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract features in the exact order used during training
        features = [
            serializer.validated_data['temperature_celsius'],
            serializer.validated_data['humidity'],
            serializer.validated_data['precip_mm'],
            serializer.validated_data['wind_kph'],
            serializer.validated_data['pressure_mb'],
        ]

        # ----- Prediction -----
        try:
            disaster_type, class_idx = predict_disaster(features)
        except Exception as e:
            logger.exception("Prediction failed")
            return Response(
                {"error": "Prediction service unavailable", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # ----- Decision Support -----
        support = get_decision_support(disaster_type)

        # ----- SHAP Explanation -----
        try:
            shap_explanation = get_shap_explanation(features, class_idx)
        except Exception as e:
            logger.warning("SHAP explanation failed: %s", e)
            shap_explanation = None

        # ----- Save prediction history (optional, fails silently) -----
        try:
            PredictionHistory.objects.create(
                user=request.user,
                temperature=features[0],
                humidity=features[1],
                precip_mm=features[2],
                wind_kph=features[3],
                pressure_mb=features[4],
                predicted_disaster=disaster_type
            )
        except Exception as e:
            logger.warning("Failed to save prediction history: %s", e)
            # Do not affect the response

        # ----- Build response -----
        response_data = {
            "disaster_type": disaster_type,
            "recommendation": support["recommendation"],
            "actions": support["actions"],
            "shap_explanation": shap_explanation,
            "message": f"Prediction based on current weather parameters. ({disaster_type} risk detected)"
        }

        response_serializer = PredictionResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)