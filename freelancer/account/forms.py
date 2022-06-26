import email
from django import forms
from django.contrib.auth import get_user_model

class UserRegister(forms.Form):
    full_name = forms.CharField(max_length=70 , widget=forms.TextInput(attrs={"class":"input-text" ,"placeholder":"نام و نام خانوادگی"}))
    username = forms.CharField(max_length=70 , widget=forms.TextInput(attrs={"class":"input-text" ,"placeholder":"نام کاربری"}))
    email = forms.CharField(max_length=70 , widget=forms.EmailField(attrs={"class":"input-text" ,"placeholder":"ایمیل"}))
    password = forms.CharField(max_length=100 ,widget=forms.PasswordInput(attrs={"placeholder":"* رمز عبور", "class":"input-text"}))
    password2 = forms.CharField(max_length=100 ,widget=forms.PasswordInput(attrs={"placeholder":"* رمز عبور", "class":"input-text"}))


    def clean_email(self):
        email = self.cleaned_data["email"]
        user = get_user_model().objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("این ایمیل قبلا در سایت ثبت نام کرده است")
        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = get_user_model().objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError("این یوزرنیم از قبل در سایت وجود دارد")
        return username


        