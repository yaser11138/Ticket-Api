from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("user/<int:id>/", UserView.as_view(), name="user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]