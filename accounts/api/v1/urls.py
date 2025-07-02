from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'api-v1'

urlpatterns = [
    path('registeration/', views.RegistrationApiView.as_view(), name='register'),
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token_login'),
    path('token/logout/', views.CustomTokenDiscardView.as_view(), name='token_logout'),

    #change password user
    path('change_password/' , views.MyChangePasswordView.as_view(), name='change_password'),
    #show profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),

    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/create/',views.CustomObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

]