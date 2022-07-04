import re
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddJobForm, EditJobForm, ApplayForm
from .models import Job, Apply


def pagination(object_list, per_page: int, page_number: int):
    paginator = Paginator(object_list=object_list, per_page=per_page)
    jobs = paginator.get_page(number=page_number)

    context = {
        'jobs': jobs
    }
    return context


def Home(request):
    return render(request, 'job/home/index.html')


def add_job(request, success_url="job:manage-job", form_class=AddJobForm, template_name='job/add-job.html'):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
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
    page_number = request.GET.get('page')
    jobs = Job.objects.filter(user=request.user).order_by("-created")
    context = pagination(object_list=jobs, per_page=5, page_number=page_number)

    return render(request=request, template_name=template_name, context=context)


def detail_job(request, id, template_name='job/detail-job.html'):
    job = get_object_or_404(klass=Job, id=id)
    context = {'job': job}
    return render(request=request, template_name=template_name, context=context)


def edit_job(request, id, success_url="job:manage-job", form_class=EditJobForm, template_name='job/edit-job.html'):
    job = get_object_or_404(klass=Job, user=request.user, id=id)
    
    if request.method == 'POST':
        form = form_class(data=request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect(success_url)
        
        context = {'forms': form}
        return render(request=request, template_name=template_name, context=context)
        
    else:
        form = form_class(instance=job)
        context = {'forms': form}
        return render(request=request, template_name=template_name, context=context)


def delete_job(request, id, success_url="job:manage-job"):
    """
        Using the `GET` request method to delete the user job.
    """
    if request.method == "GET":
        job = get_object_or_404(klass=Job, user=request.user, id=id).delete()

        return JsonResponse({
            "delete-job": True,
        })


def applay_to(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == 'POST':
        if request.user == job.user:
            return redirect('job:home')

        form = ApplayForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            applay = Apply.objects.create(
                user = request.user,
                job=job,
                description=cd['description'],
                price=cd['price'],
                finish_time=cd['finish_time'],
            )
            applay.save()
    else:
        form = ApplayForm()
    
    context = {
        'form': form
    }
    return render(request, 'job/applay-to.html', context=context)