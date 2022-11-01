from .filters import ProjectFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from django.contrib.auth import login, logout

# Filters
from django_filters import rest_framework as filters


# Api Doc
from drf_spectacular.utils import extend_schema_view, extend_schema

# Models
from freelancer.account.models import User, Profile
from freelancer.resume.models import CV, Education, WorkExperience, Contact
from freelancer.project.models import Project

# Serializers
from .serializer import (LoginUserSerializer, RegisterUserSerializer, UserInfoSerializer, UserSerializer,
                         ProfileSerializer, ResumeSerializer, WorkExperienceSerializer, EducationSerializer,
                         ContactSerializer, ProjectSerializer)


@extend_schema_view(post=extend_schema(summary="Login User"))
class LoginUser(APIView):
    http_metod_names = ["post"]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(user=serializer.validated_data, request=request)
        return Response(data={"message": "Login successful"}, status=status.HTTP_200_OK)


@extend_schema_view(create=extend_schema(summary="Register New User"))
class RegisterUser(ViewSet):
    http_method_names = ["post"]
    serializer_class = RegisterUserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(post=extend_schema(summary="Logout User"))
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


@extend_schema_view(
    get=extend_schema(summary="User Info"),
    put=extend_schema(summary="User Info", tags=["profile"]),
    patch=extend_schema(summary="User Partial Update", tags=["profile"])
)
class UserInfo(RetrieveUpdateAPIView):
    """Get and udapte the user data"""
    permission_classes = (IsAuthenticated, )
    http_method_names = ("put", "patch", "get")
    queryset = User.objects.all()
    lookup_field = "username"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserSerializer
        else:
            return UserInfoSerializer


@extend_schema(methods=["put", "patch"], summary="User Profile", tags=["profile"])
class UpdateUserProfile(BaseUpdateView):
    """Update the full user profile or partial update"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__username"


@extend_schema(methods=["put", "patch"], summary="User Resume", tags=["resume"])
class UpdateUserResume(BaseUpdateView):
    """Update the full resume or partial update"""
    queryset = CV.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = "user__username"


@extend_schema(methods=["put", "patch"], summary="User Experiences", tags=["resume"])
class UpdateResumeExperiences(BaseUpdateView):
    """Update the full resume work-experiences or partial update"""
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


@extend_schema(methods=["put", "patch"], summary="User Educations", tags=["resume"])
class UpdateResumeEducations(BaseUpdateView):
    """Update the full resume education or partial update"""
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


@extend_schema(methods=["put", "patch"], summary="User Contacts", tags=["resume"])
class UpdateResumeContacts(BaseUpdateView):
    """Update the full resume contacts or partial update"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


@extend_schema(methods=["get", "post"], summary="Create and list User Project", tags=["projects"])
class ListProject(ListAPIView, CreateAPIView):
    """Get list of projects"""
    http_method_names = ("get", "post")
    permission_classes = (IsOwnerOrReadOnly, )
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter
    queryset = Project.objects.all()


@extend_schema(methods=["get", "post", "put", "patch", "delete"], summary="CRUD specific Project", tags=["projects"])
class ProjectDetail(RetrieveUpdateDestroyAPIView):
    """CRUD specific Project with id"""
    http_method_names = ("get", "put", "patch", "delete")
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ProjectSerializer
    lookup_url_kwarg = "project_id"

    def get_queryset(self):
        return Project.objects.filter(pk=self.kwargs["project_id"])
