from aiohttp import request
from django.shortcuts import render


def login_user(request):
    return render(request, 'account/login.html')



def register_user(request):
    return render(request, 'account/register.html')
