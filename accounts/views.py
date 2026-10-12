from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from accounts.serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Email and password are required'},status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request,username=username,password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)

    return Response({'message': 'Login successful','refresh': str(refresh),'access': str(refresh.access_token),}, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({'error': 'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Logout successful'},status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid or expired refresh token'},status=status.HTTP_400_BAD_REQUEST)
