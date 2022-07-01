from django.shortcuts import render

from .forms import AddJobForm
from .models import Job
from django.utils.text import slugify

def Home(request):
    return render(request, 'job/home/index.html')


def add_job(request, form_class=AddJobForm, template_name='job/add-job.html'):
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            job = Job.objects.create(
                user=request.user,
                category=cd['category'],
                title=cd['title'],
                company_name=cd['company_name'],
                slug=slugify(cd['title']),
                tags=cd['tags'],
                description=cd['description'],
                place=cd['place'],
                work_type=cd['work_type'],
                image=cd['image'],
                price=cd['price']
            )
            job.save()
            

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
