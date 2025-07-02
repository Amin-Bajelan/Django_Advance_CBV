from django.shortcuts import get_object_or_404
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import RegistrationSerialize, CustomTokenDiscardSerializer, ChangePasswordView, ProfileSerializer, \
    ActivationSerializerApiView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.views import (
    TokenObtainPairView, )

from ...models import User, Profile
from ..utils import EmailThreading

from django.core.mail import send_mail
from mail_templated import send_mail
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerialize

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
            data = {
                'email': email,
                'message': 'Your account has been created successfully.',
            }
            user_obj = get_object_or_404(User, email=serializer.data['email'])
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl',
                                     {'token': token}, 'amin@gmail.com', [email])
            EmailThreading(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


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


class TestSendEmail(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        # send_mail(
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        # )
        self.email = 'bajelan@gmail.com'
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl',
                                 {'token': token}, 'amin@gmail.com', ['m.amin.bajelan@gmail.com'])
        EmailThreading(email_obj).start()
        return Response('email send successfully.')

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({"detail": "token expirdsignature error"}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidTokenError:
            return Response({"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        obj_user = get_object_or_404(User, id=user_id)
        if obj_user.is_verified:
            return Response("your account has already been verified", status=status.HTTP_200_OK)
        obj_user.is_verified = True
        obj_user.save()
        return Response("Successfully activated")

class ResendActivationView(generics.GenericAPIView):
    serializer_class = ActivationSerializerApiView
    def post(self, request, *args, **kwargs):
            serializer = ActivationSerializerApiView(data=request.data)

            if serializer.is_valid():
                user_obj = serializer.data['user']
                token = self.get_tokens_for_user(user_obj)
                email_obj = EmailMessage('email/hello.tpl',
                                         {'token': token}, 'amin@gmail.com', ['m.amin.bajelan@gmail.com'])
                EmailThreading(email_obj).start()
                return Response({"detail": "user activation send successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail":'there is some error'}, status=status.HTTP_400_BAD_REQUEST)
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)