from django.shortcuts import render

from .forms import AddJobForm
from .models import Job


def Home(request):
    return render(request, 'job/home/index.html')


def add_job(request, form_class=AddJobForm, template_name='job/add-job.html'):
    if request.method == 'POST':
        pass
    else:
        form = form_class

    context = {'forms': form}
    return render(request=request, template_name=template_name, context=context)


def manage_job(request, template_name='job/manage-job.html'):
    jobs = Job.objects.filter(user=request.user)
    context = {'jobs': jobs}
    return render(request=request, template_name=template_name, context=context)


def edit_job(request, id):
    pass


def delete_job(request, id):
    pass
