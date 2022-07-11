from django.shortcuts import render
from .models import Faq

def faq(request):
    
    faqs = Faq.objects.all().order_by('position')
    context = {
        'faqs' : faqs
    }
    return render(
        request=request, 
        template_name='faq/faq.html',
        context=context
    )