from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import login
from .serializer import LoginUserSerializer, RegisterUserSerializer


class LoginUser(APIView):
    http_metod_names = ["post"]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(user=serializer.validated_data, request=request)
        return Response(data={"Login": "Successfully"}, status=status.HTTP_200_OK)


class RegisterUser(ViewSet):
    http_method_names = ["post"]
    serializer_class = RegisterUserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)