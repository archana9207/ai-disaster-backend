from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Read/update the current user's profile (username, email)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def validate_username(self, value):
        qs = User.objects.exclude(pk=self.instance.pk).filter(username=value)
        if qs.exists():
            raise serializers.ValidationError('A user with that username already exists.')
        return value

    def validate_email(self, value):
        qs = User.objects.exclude(pk=self.instance.pk).filter(email=value)
        if qs.exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Validates current + new password for a password-change request."""
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user)
        return value