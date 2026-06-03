from django.urls import path
from .views import PredictDisasterView

urlpatterns = [
    path('', PredictDisasterView.as_view(), name='predict'),
]