from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import *


app_name = "api"

urlpatterns = [
    # path('', home_page, name='home'),
    path('auth/login/', LoginUser.as_view(), name='login'),
    path('auth/register/', RegisterUser.as_view({"post": "create"}), name='Register'),


    # path('register/', register_user, name='register'),
    # path('logout/', logout_user, name='logout'),

    # path('dashboard/', dashboard, name='dashboard'),
    # path('dashboard/messages/', user_messages, name='messages'),
    # path('dashboard/edit-profile/', edit_profile, name='edit-profile'),
    # path('dashboard/manage-project/', manage_project, name='manage-project'),
    # path('dashboard/manage-received-applys/', manage_received_apply, name='manage-received-apply'),
    # path('dashboard/manage-send-applys/', manage_send_apply, name='manage-send-apply'),
]