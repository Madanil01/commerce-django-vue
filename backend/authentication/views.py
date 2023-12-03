from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from datetime import datetime, timedelta

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        # Set expiration time to 5 minutes (adjust as needed)
        expiration_time = timedelta(days=1)

        # Generate access token with specified expiration time
        token = RefreshToken.for_user(user)
        token.access_token.set_exp(lifetime=expiration_time)

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username + ' Use link below to verify your email \n' + abs_url
        data = {'email_body': email_body, 'email_to': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    

class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        expiration_time = datetime.now() + timedelta(days=1)

        # Generate access token
        access_token = RefreshToken.for_user(user).access_token

        # Include the token in the response's cookies
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie('access_token', str(access_token), expires=expiration_time, secure=True)

        # Serialize the user object
        user_serializer = UserSerializer(user)
        response.data = {
            'access_token': str(access_token),
            'user': user_serializer.data
        }

        return response

class UserView(generics.GenericAPIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.get(id=payload['user_id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(generics.GenericAPIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')

        response.data = {
            'message': 'success'
        }
        return response