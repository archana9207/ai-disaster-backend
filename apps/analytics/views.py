from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import (
    PredictionHistorySerializer,
    AnalyticsSummarySerializer,
)
from .utils import (
    get_disaster_breakdown,
    get_most_common_disaster,
    get_monthly_trends,
    get_recent_predictions,
    get_total_predictions,
)


class PredictionHistoryView(APIView):
    """
    GET /api/analytics/history/
    Returns list of user's past predictions.
    Query param: ?limit=20 (default 10, max 100)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = request.query_params.get('limit', 10)
        try:
            limit = min(int(limit), 100)
        except (ValueError, TypeError):
            limit = 10

        history = get_recent_predictions(request.user, limit=limit)
        serializer = PredictionHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnalyticsSummaryView(APIView):
    """
    GET /api/analytics/summary/
    Returns overall statistics, disaster breakdown, monthly trends,
    and recent predictions.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        summary_data = {
            'total_predictions': get_total_predictions(user),
            'disaster_breakdown': get_disaster_breakdown(user),
            'most_common_disaster': get_most_common_disaster(user),
            'recent_predictions': PredictionHistorySerializer(
                get_recent_predictions(user, limit=5), many=True
            ).data,
            'monthly_trends': get_monthly_trends(user, months_back=6),
        }

        serializer = AnalyticsSummarySerializer(data=summary_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)