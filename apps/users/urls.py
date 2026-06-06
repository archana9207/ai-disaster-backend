from django.urls import path
from .views import UserProfileView, ChangePasswordView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]