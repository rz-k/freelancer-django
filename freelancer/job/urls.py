from unicodedata import name
from django.urls import path
from .views import *


app_name = 'job'
urlpatterns = [
    path('', Home, name='home')
]