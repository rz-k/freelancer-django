from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .forms import AddProjectForm, EditProjectForm, ApplyProjectForm
from .models import ApplyProject, Project
from django.http import JsonResponse
from django.contrib import messages



def add_project(request, success_url="account:manage-job", form_class=AddProjectForm, template_name='project/add-proj.html'):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data          
            Project.objects.create(
                user=request.user,
                category=cd['category'],
                title=cd['title'],
                slug=cd['title'],
                tags=cd['tags'],
                description=cd['description'],
                budget=cd['budget'],
                urgent=cd['urgent'],
                highlight=cd['highlight'],
                private=cd['private']
            )
            return redirect(success_url)
    else:
        form = form_class()
    context = {'forms': form}
    return render(request=request, template_name=template_name, context=context)


def edit_project(request, id, success_url="account:manage-job", form_class=EditProjectForm, template_name='project/edit-proj.html'):
    project = get_object_or_404(klass=Project, user=request.user, id=id)
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect(success_url)
        context = {'forms': form}
        return render(request=request, template_name=template_name, context=context)

    else:
        form = form_class(instance=project)
        context = {'forms': form}
        return render(request=request, template_name=template_name, context=context)


def detail_project(request, id, form_class=ApplyProjectForm, template_name='project/detail-proj.html'):
    project = get_object_or_404(klass=Project, id=id)
    if not project.paid :
        if request.user != project.user:
            return redirect('job:home')

    form = form_class()
    is_employer = False
    if request.user == project.user:
        is_employer = True

    context = {
        "project": project,
        "is_employer": is_employer,
        "apply_form": form}
    return render(request=request, template_name=template_name, context=context)


def delete_project(request, id, success_url="account:manage-job"):
    """
        Using the `GET` request method to delete the user job.
    """
    if request.method == "GET":
        get_object_or_404(klass=Project, user=request.user, id=id).delete()
        return JsonResponse({
            "delete-job": True,
        })


def apply_to(request, id, next_url="job:home", success_url="job:detail-job", form_class=ApplyProjectForm, template_name='job/detail-job.html'):
    project = get_object_or_404(klass=Project, id=id)

    if request.method == "POST":
        if request.user == project.user:
            return redirect(next_url)

        form = form_class(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            apply = ApplyProject.objects.create(
                user = request.user,
                project=project,
                description=cd['description'],
                bid_amount=cd['bid_amount'],
                bid_date=cd['bid_date']
                )
            messages.success(request=request, message="درخواست شما برای گرفتن این پروژه ارسال شد", extra_tags="success")
            return redirect(next_url)

        messages.error(request=request, message="لطفا مقادیر گفته شده را به درستی وارد نمایید.", extra_tags="danger")
        return redirect(success_url, project.id)
    else:
        form = form_class()
        return render(request=request, template_name=template_name, context={"apply_form": form})
