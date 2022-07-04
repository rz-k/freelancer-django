from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    
    path('dashboard/user-messages/', user_messages, name='user-messages'),
    path('dashboard/edit-profile/', edit_profile, name='edit-profile'),
    
    path('dashboard/', dashboard, name='dashboard'),

    path('dashboard/manage-candidate/', manage_candidate, name='manage-candidate'),
    path('dashboard/manage-applays/', manage_applay_send, name='manage-applay-send'),
]
