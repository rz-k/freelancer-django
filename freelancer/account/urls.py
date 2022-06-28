from django.urls import path

from .views import (add_job, dashboard, edit_profile, login_user, logout_user,
                    manage_candidate, manage_job, register_user, user_messages)

app_name = 'account'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add-job/', add_job, name='add-job'),
    path('dashboard/manage-job/', manage_job, name='manage-job'),
    path('dashboard/manage-candidate/', manage_candidate, name='manage-candidate'),
    path('dashboard/user-messages/', user_messages, name='user-messages'),
    path('dashboard/edit-profile/', edit_profile, name='edit-profile'),
]