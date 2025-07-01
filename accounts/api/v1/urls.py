from django.urls import path, include
from . import views


app_name = 'api-v1'

urlpatterns = [
    path('registeration/', views.RegistrationApiView.as_view(), name='register'),
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token_login'),
    path('token/logout/', views.CustomTokenDiscardView.as_view(), name='token_logout'),

]