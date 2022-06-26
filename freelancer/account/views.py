from xml.dom import ValidationErr
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_user(request):
    if request.user.is_authenticated:
        return redirect('job:home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            user = authenticate(
                request, 
                email=cd['email'],
                password=cd['password']
            )
            if user is not None:
                login(request, user=user)
                messages.success(request, 'با موفقیت لاگین شدین')
                return redirect('job:home')
            else:
                messages.error(request, "ورود به حساب کاربر با خطا مواجه شد، لطفا یوزرنیم و پسورد خود را چک کنید.")
                return render(request, 'account/login.html', {"form_login": form})
    else:
        form = UserLoginForm()
    context = {
        'form_login': form
    }
    return render(request, 'account/login.html', context=context)



def register_user(request):
    return render(request, 'account/register.html')
