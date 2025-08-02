from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('verify/resend/', ResendVerificationEmailView.as_view()),
    path('verify/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
]
