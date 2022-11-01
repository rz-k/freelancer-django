from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
from rest_framework.routers import DefaultRouter


app_name = "api"

urlpatterns = [
    # path('', home_page, name='home'),

    # Atuh
    path('users/login/', LoginUser.as_view(), name='login'),
    path('users/register/', RegisterUser.as_view({"post": "create"}), name='register'),
    path('users/logout/', LogoutUser.as_view(), name='logout'),

    # Profile
    path('users/<str:username>/', UserInfo.as_view(), name='user-info'),
    path('users/<str:username>/profile/', UpdateUserProfile.as_view(), name='update-user-profile'),
    path('users/<str:username>/resume/', UpdateUserResume.as_view(), name='update-user-resume'),
    path('users/<str:username>/resume/experiences/', UpdateResumeExperiences.as_view(), name='update-resume-experiences'),
    path('users/<str:username>/resume/educations/', UpdateResumeEducations.as_view(), name='update-resume-educations'),
    path('users/<str:username>/resume/contacts/', UpdateResumeContacts.as_view(), name='update-resume-contacts'),

    # Project
    path("projects/", ListProject.as_view(), name="list-projet"),
    path("projects/<int:project_id>/", ProjectDetail.as_view(), name="project-details"),

    # path("project/categorys/", RetrieveCategorys.as_view(), name="retrieve-categorys"),
    # path("project/categorys/", AddCategorys.as_view(), name="retrieve-categorys"),
    # path("project/<int:pk>/employers-comment/", RetrieveEmployersComment.as_view(), name="retrieve-employers-comment"),
    # path("project/<int:pk>/employers-comment/", UpdateEmployersComment.as_view(), name="update-employers-comment"),
    # path("project/<int:pk>/conversation/", RetrieveProjectConversation.as_view(), name="retrieve-project-conversation"),
    # path("project/<int:pk>/conversation/", UpdateProjectConversation.as_view(), name="update-project-conversation"),
    # path('dashboard/manage-project/', manage_project, name='manage-project'),
    # path('dashboard/manage-received-applys/', manage_received_apply, name='manage-received-apply'),
    # path('dashboard/manage-send-applys/', manage_send_apply, name='manage-send-apply'),
]
