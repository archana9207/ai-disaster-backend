from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        # Return first error as 'detail' for frontend
        first_error = list(serializer.errors.values())[0][0] if serializer.errors else 'Registration failed'
        return Response({'detail': first_error}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {'id': user.id, 'username': user.username, 'email': user.email}
            }, status=status.HTTP_200_OK)
        first_error = list(serializer.errors.values())[0][0] if serializer.errors else 'Invalid credentials'
        return Response({'detail': first_error}, status=status.HTTP_400_BAD_REQUEST)