from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegisterForm
from freelancer.job.models import Apply


def login_user(request, next_url='account:dashboard', form_class=UserLoginForm, template_name="account/login.html"):
    """
    Login user to the account

    Args:
        next_url (str):
            This is a success_url to redirect logged-in users.

        form_class (Form, optional): 
            User Login Form.
            
        template_name (str, optional):
            Name of the template to be rendered in this view.
    """
    success_url = redirect(next_url)
    if request.user.is_authenticated:
        return success_url
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data  
            user = authenticate(
                request=request, 
                email=cd['email'],
                password=cd['password'])
            
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message='شما با موفقیت لاگین شدید', extra_tags="success")
                return success_url
            else:
                messages.error(request=request, message="یوزرنیم یا پسورد وارد شده اشتباه است!", extra_tags="danger")
                return render(request=request,
                    template_name=template_name,
                    context={"form_login": form})

    else:
        form = form_class()
    context = {'form_login': form}
    
    return render(request=request,
        template_name=template_name,
        context=context)


def register_user(request, next_url='account:dashboard', form_class=UserRegisterForm, template_name='account/register.html'):
    """
    Register new user(sign up).

    Args:
        next_url (str):
            This is a success_url to redirect logged-in users.

        form_class (Form, optional): 
            User Register Form.
            
        template_name (str, optional):
            Name of the template to be rendered in this view.
    """
    success_url = redirect(next_url)
    if request.user.is_authenticated:
        return success_url
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user =  get_user_model().objects.create_user(
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                username=cd['username'],
                email=cd['email'],
                password=cd['password'],
            )
            user.is_active = True
            user.save()
            messages.success(request=request, message="ثبت نام با موفقیت انجام شد.", extra_tags="success")
            return success_url
        else:
            messages.error(request=request, message="موارد گفته شده را به درستی وارد نمایید", extra_tags="danger")
            return render(request=request,
                    template_name=template_name,
                    context={"form_register": form})
    else:
        form = form_class()

    context = {'form_register': form}
    
    return render(request=request,
        template_name=template_name,
        context=context)


def logout_user(request):
    """
    Logged out the user and redirect to the home page
    """
    logout(request)
    messages.success(
        request=request,
        message='خروج از حساب کاربری با موفقیت انجام شد.', 
        extra_tags="success")
    return redirect("job:home")



def dashboard(request, template_name='account/dashboard/dashboard.html'):
    return render(request=request, template_name=template_name)


def manage_candidate(request, template_name='account/dashboard/manage-candidate.html'):
    applays = Apply
    return render(request, template_name=template_name)


def user_messages(request, template_name='account/dashboard/user-messages.html'):    
    return render(request, template_name=template_name)


def edit_profile(request, template_name='account/dashboard/edit-profile.html'):
    return render(request, template_name=template_name)


