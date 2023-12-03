from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView, UserView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user', UserView.as_view(), name='user'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify'),
]