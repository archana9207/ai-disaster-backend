from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import IntegrityError

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_email(self, value):
        # BUG FIX: the User model declares email as unique=True, but the
        # original serializer had no explicit uniqueness check. When a duplicate
        # email was submitted Django raised an IntegrityError (unhandled
        # database exception) → 500.  Validate here so DRF returns a clean 400.
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_username(self, value):
        # Same issue for username — AbstractUser marks it unique but DRF won't
        # surface that as a 400 without explicit validation.
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )
            return user
        except IntegrityError as e:
            # Last-resort safety net for any race-condition duplicates
            raise serializers.ValidationError(
                {"detail": "Account creation failed. Username or email already in use."}
            ) from e


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password'],
        )
        if not user:
            # BUG FIX: original raised ValidationError with a plain string.
            # DRF wraps that under the key "non_field_errors", but the frontend
            # was looking for "detail". Raise with detail key so the frontend
            # error message works correctly.
            raise serializers.ValidationError({"detail": "Invalid username or password."})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "This account has been disabled."})
        data['user'] = user
        return data