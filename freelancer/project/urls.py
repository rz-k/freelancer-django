from django.urls import path
from .views import *


app_name = 'project'
urlpatterns = [
    path('add/', add_project, name='add-project'),
    path('edit/<int:id>', edit_project, name='edit-project'),
    path('visit/<int:id>', detail_project, name='detail-project'),
    path('delete/<int:id>', delete_project, name='delete-project'),
]