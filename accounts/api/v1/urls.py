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

    path('test-email/',views.TestSendEmail.as_view(), name='test_email'),
    #activation
    path('activation/send/<str:token>',views.ActivationApiView.as_view(), name='send_activation'),
    #resend activation
    path('resend/activation/<str:token>',views.ResendActivationView.as_view(), name='resend_activation'),

]