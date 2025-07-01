from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import RegistrationSerialize
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



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
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
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