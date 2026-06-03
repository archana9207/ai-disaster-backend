from rest_framework import serializers
from apps.prediction.models import PredictionHistory

class PredictionHistorySerializer(serializers.ModelSerializer):
    """Serializes a single prediction record."""
    class Meta:
        model = PredictionHistory
        fields = [
            'id', 'temperature', 'humidity', 'precip_mm',
            'wind_kph', 'pressure_mb', 'predicted_disaster', 'created_at'
        ]


class DisasterBreakdownSerializer(serializers.Serializer):
    """Disaster type count."""
    disaster_type = serializers.CharField()
    count = serializers.IntegerField()


class MonthlyTrendSerializer(serializers.Serializer):
    """Monthly trend data for frontend charts."""
    month = serializers.CharField()          # "YYYY-MM"
    counts = serializers.DictField(child=serializers.IntegerField())
    total = serializers.IntegerField()


class AnalyticsSummarySerializer(serializers.Serializer):
    """Full analytics summary response."""
    total_predictions = serializers.IntegerField()
    disaster_breakdown = DisasterBreakdownSerializer(many=True)
    most_common_disaster = serializers.CharField(allow_null=True)
    recent_predictions = PredictionHistorySerializer(many=True)
    monthly_trends = MonthlyTrendSerializer(many=True)