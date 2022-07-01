from django.urls import path
from freelancer.job.views import add_job, delete_job, edit_job, manage_job

from .views import (dashboard, edit_profile, login_user, logout_user,
                    manage_candidate, register_user, user_messages)

app_name = 'account'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add-job/', add_job, name='add-job'),
    path('dashboard/delete-job/', add_job, name='delete-job'),
    path('dashboard/edit-job/', add_job, name='edit-job'),
    path('dashboard/manage-job/', manage_job, name='manage-job'),

    path('dashboard/manage-candidate/', manage_candidate, name='manage-candidate'),

    path('dashboard/user-messages/', user_messages, name='user-messages'),
    path('dashboard/edit-profile/', edit_profile, name='edit-profile'),
]
