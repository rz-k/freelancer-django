from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddJobForm, EditJob
from .models import Job


def Home(request):
    return render(request, 'job/home/index.html')


def add_job(request, success_url="account:manage-job", form_class=AddJobForm, template_name='job/add-job.html'):
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_job = Job.objects.create(
                user=request.user,
                category=cd['category'],
                title=cd['title'],
                company_name=cd['company_name'],
                slug=cd['title'],
                tags=cd['tags'],
                description=cd['description'],
                place=cd['place'],
                work_type=cd['work_type'],
                image=cd['image'],
                price=cd['price']
            )
            return redirect(success_url)
    else:
        form = form_class()

    context = {'forms': form}
    return render(request=request, template_name=template_name, context=context)


def manage_job(request, template_name='job/manage-job.html'):
    jobs = Job.objects.filter(user=request.user).order_by("-created")
    context = {'jobs': jobs}
    return render(request=request, template_name=template_name, context=context)


def detail_job(request, id, template_name='job/detail-job.html'):
    job = get_object_or_404(klass=Job, id=id)
    context = {'job': job}
    return render(request=request, template_name=template_name, context=context)


def edit_job(request, id, form_class=EditJob,template_name='job/edit-job.html'):
    job = get_object_or_404(klass=Job, user=request.user, id=id)
    if request.method == 'POST':
        pass
    else:

    # form = form_class(instance=job)
        form = form_class(request.POST, instance = job)
        context = {
            'forms': form
        }
    
    return render(request, template_name, context=context)



def delete_job(request, id, success_url="account:manage-job"):
    job = get_object_or_404(klass=Job, user=request.user, id=id)
    job.delete()
    return redirect(success_url)   
