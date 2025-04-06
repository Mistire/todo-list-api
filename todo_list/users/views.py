from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user and return an authentication token",
        request_body=RegisterSerializer
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: 'JWT Token'}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Use get_user_model to handle custom user models
            User = get_user_model()

            try:
                # Retrieve user by email
                user = User.objects.get(email=email)

                # Check if the password is correct
                if user.check_password(password):
                    # Generate JWT token for the user
                    refresh = RefreshToken.for_user(user)
                    return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
                else:
                    # Invalid credentials error
                    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                # User doesn't exist, invalid credentials error
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # If serializer is not valid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)