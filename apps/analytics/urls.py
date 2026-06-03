from django.urls import path
from .views import PredictionHistoryView, AnalyticsSummaryView

urlpatterns = [
    path('history/', PredictionHistoryView.as_view(), name='prediction-history'),
    path('summary/', AnalyticsSummaryView.as_view(), name='analytics-summary'),
]