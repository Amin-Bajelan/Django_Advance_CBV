from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import RegistrationSerialize, CustomTokenDiscardSerializer, ChangePasswordView, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.views import (
    TokenObtainPairView, )

from ...models import User, Profile


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerialize

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.data['email'],
                'message': 'Your account has been created successfully.',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
        })


class CustomTokenDiscardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenDiscardSerializer


class MyChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordView
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordView(data=request.data)

        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["your old password is wrong"]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({"detail": "password change successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user)
        return obj
