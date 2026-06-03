from rest_framework import serializers

class WeatherInputSerializer(serializers.Serializer):
    """
    Serializer for weather data input from the user.
    Features must match exactly the five used during model training.
    """
    temperature_celsius = serializers.FloatField(
        help_text="Air temperature in Celsius",
        min_value=-50.0,
        max_value=60.0
    )
    humidity = serializers.IntegerField(
        help_text="Relative humidity (%)",
        min_value=0,
        max_value=100
    )
    precip_mm = serializers.FloatField(
        help_text="Precipitation in millimeters",
        min_value=0.0
    )
    wind_kph = serializers.FloatField(
        help_text="Wind speed in km/h",
        min_value=0.0
    )
    pressure_mb = serializers.FloatField(
        help_text="Atmospheric pressure in millibars",
        min_value=800.0,
        max_value=1100.0
    )


class PredictionResponseSerializer(serializers.Serializer):
    """
    Serializer for the prediction API response.
    """
    disaster_type = serializers.CharField()
    recommendation = serializers.CharField()
    actions = serializers.ListField(child=serializers.CharField())
    shap_explanation = serializers.DictField(
        child=serializers.FloatField(),
        required=False,
        allow_null=True
    )
    message = serializers.CharField(required=False)