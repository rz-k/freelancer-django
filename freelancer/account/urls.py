from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [


    path('', Home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/messages/', user_messages, name='messages'),
    path('dashboard/edit-profile/', edit_profile, name='edit-profile'),
    path('dashboard/manage-project/', manage_project, name='manage-project'),
    path('dashboard/manage-candidate/', manage_candidate, name='manage-candidate'),
    path('dashboard/manage-applays/', manage_applay_send, name='manage-applays'),


    path('profile/<str:username>/', candidate_profile, name='candidate-profile'),

]
