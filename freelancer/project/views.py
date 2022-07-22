from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, redirect, render
from freelancer.pricing.models import ActivePricingPanel, PricingPanel

from .forms import AddProjectForm, ApplyProjectForm, EditProjectForm
from .models import ApplyProject, Project


def add_project(request, success_url="account:manage-project", form_class=AddProjectForm, template_name='project/add-project.html'):
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


def edit_project(request, id, success_url="account:manage-project", form_class=EditProjectForm, template_name='project/edit-proj.html'):
    project = get_object_or_404(klass=Project, user=request.user, id=id)
    if project.paid:
        if project.publish == 'wait' or project.publish == 'publish':
            return redirect(success_url)
    
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
            return redirect("account:home")

    form = form_class()
    is_employer = False
    if request.user == project.user:
        is_employer = True

    context = {
        "project": project,
        "is_employer": is_employer,
        "apply_form": form}
    return render(request=request, template_name=template_name, context=context)


def delete_project(request, id, success_url="account:manage-project"):
    """
        Using the `GET` request method to delete the user project.
    """
    if request.method == "GET":
        get_object_or_404(klass=Project, user=request.user, id=id).delete()
        return JsonResponse({
            "delete-project": True,
        })


def check_active_pricing_panel(request) -> bool:
    """
    Check the Expire time and apply count of the active pricing panel,
    if the user has enough apply count then increase the apply counter
    otherwise return an error.
    """
    active_panel =  ActivePricingPanel.objects.get(user=request.user)
    if active_panel.is_expire():
        messages.success(
            request=request,
            message="زمان پنل شما به اتمام رسیده است، جهت خرید پنل جدید میتوایند از قسمت پنل ها اقدام نمایید",
            extra_tags="danger")
        return False
    else:
        if active_panel.has_apply():
            active_panel.count += 1
            active_panel.save()
            return True
        else:
            messages.success(
                request=request,
                message="تعداد درخواست های پنل فعلی شما به پایان رسیده است، جهت خرید پنل جدید میتوایند از قسمت پنل ها اقدام نمایید",
                extra_tags="danger")
            return False


def apply_to(request, id, next_url="account:home",
            success_url="project:detail-project", form_class=ApplyProjectForm,
            template_name='project/detail-proj.html'):
    """
    Check the active pricing panel of sender user and then
    create a new apply for him or return an error.
    """

    active_panel_status = check_active_pricing_panel(request=request)
    if active_panel_status == False:
        return redirect(success_url, id)

    project = get_object_or_404(klass=Project, id=id)
    if request.method == "POST":
        # Redirect if user is creator of the project.
        if request.user == project.user:
            return redirect(next_url)
        else:
            form = form_class(data=request.POST)
            if form.is_valid():
                form.save(project=project, sender_user=request.user)
                messages.success(
                    request=request,
                    message="درخواست شما برای گرفتن این پروژه ارسال شد",
                    extra_tags="success")
                return redirect(next_url)
            else:
                messages.error(
                    request=request,
                    message="لطفا مقادیر گفته شده را به درستی وارد نمایید.", 
                    extra_tags="danger")
                return redirect(success_url, project.id)
    else:
        form = form_class()
        return render(request=request,
                      template_name=template_name,
                      context={"apply_form": form})