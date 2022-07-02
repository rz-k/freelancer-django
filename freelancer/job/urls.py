from django.urls import path

from .views import *
from .views import add_job, delete_job, detail_job, edit_job, manage_job

app_name = 'job'

urlpatterns = [
    path('', Home, name='home'),
    path('account/dashboard/add-job/', add_job, name='add-job'),
    path('account/dashboard/job/<int:id>', detail_job, name='detail-job'),
    path('account/dashboard/delete-job/<int:id>', delete_job, name='delete-job'),
    path('account/dashboard/edit-job/<int:id>', edit_job, name='edit-job'),
    path('account/dashboard/manage-job/', manage_job, name='manage-job'),
]
