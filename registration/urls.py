from django.urls import path

from .views import *

urlpatterns = [
    # auth
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
