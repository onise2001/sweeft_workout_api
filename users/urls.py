from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserRegistrationView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]