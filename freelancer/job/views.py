import re
from django.shortcuts import render



def Home(request):
    return render(request, 'job/index.html')
