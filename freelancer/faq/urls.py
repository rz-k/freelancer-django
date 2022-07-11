from django.urls import path
from .views import *

app_name='faq'

urlpatterns = [
    path('', faq , name='faq')
    ]