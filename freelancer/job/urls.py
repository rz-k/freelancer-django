from django.urls import path

from .views import (Home, add_job, apply_to, delete_job, detail_job, edit_job)

app_name = 'job'

urlpatterns = [

    path('', Home, name='home'),


    path('add/', add_job, name='add-job'),
    path('delete/<int:id>', delete_job, name='delete-job'),
    path('edit/<int:id>', edit_job, name='edit-job'),
    path('visit/<int:id>', detail_job, name='detail-job'),

    path('apply-to/<int:id>', apply_to, name='apply-to'),

]
