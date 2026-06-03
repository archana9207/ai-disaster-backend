from django.db import models
from django.conf import settings

class PredictionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    precip_mm = models.FloatField()
    wind_kph = models.FloatField()
    pressure_mb = models.FloatField()
    predicted_disaster = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_disaster} at {self.created_at}"