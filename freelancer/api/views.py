from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import login, logout
from .serializer import (LoginUserSerializer, RegisterUserSerializer, UserInfoSerializer, UserSerializer,
                         ProfileSerializer, ResumeSerializer, WorkExperienceSerializer, EducationSerializer, ContactSerializer)
from freelancer.account.models import User, Profile
from freelancer.resume.models import CV, Education, WorkExperience, Contact


class LoginUser(APIView):
    http_metod_names = ["post"]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(user=serializer.validated_data, request=request)
        return Response(data={"message": "Login successful"}, status=status.HTTP_200_OK)


class RegisterUser(ViewSet):
    http_method_names = ["post"]
    serializer_class = RegisterUserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutUser(APIView):
    http_method_names = ["post"]

    def post(self, request):
        logout(request=request)
        return Response(data={"message": "Logout successful"}, status=status.HTTP_200_OK)


class BaseUpdateView(RetrieveUpdateAPIView):
    http_method_names = ("put", "patch")
    permission_classes = (IsAuthenticated, )
    lookup_field = "cv__user_id"
    lookup_url_kwarg = "username"


class UserInfo(RetrieveUpdateAPIView):
    http_method_names = ("put", "patch", "get")
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    lookup_field = "username"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserSerializer
        else:
            return UserInfoSerializer


class UpdateUserProfile(BaseUpdateView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__username"


class UpdateUserResume(BaseUpdateView):
    queryset = CV.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = "user_username"


class UpdateResumeExperiences(BaseUpdateView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class UpdateResumeEducations(BaseUpdateView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class UpdateResumeContacts(BaseUpdateView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
