from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_quill.forms import QuillFormField
from .models import Category, Job


class AddJobForm(forms.Form):
    WORK_TYPES = (
        ('None', '---------'),
        ('full_time','تمام وقت',),
        ('part_time','پاره وقت'),
        ('teleworking','دور کاری'),
        ('internship','کاراموز'),
        ('temporary','موقت')
    )
    title = forms.CharField(
        label="عنوان پروژه (کار)",
        max_length=100,
        widget=forms.TextInput(            
            attrs={"class":"input-text", "placeholder":"عنوان پروژه یا شغل"}))

    company_name = forms.CharField(
        label="اسم شرکت یا پروژه شخصی",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class":"input-text", "placeholder":"اسم شرکت (پیشفرض شخصی)"}))

    place = forms.CharField(
        label="موقعیت مکانی",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class":"input-text", "placeholder":"تهران , تهران"}))

    experience = forms.CharField(
        required=False,
        label="سابقه کار(تعداد سال)",
        widget=forms.TextInput(
            attrs={"class":"input-text", "placeholder":"بین 2 تا 3 سال"}))

    price = forms.CharField(
        max_length=100,
        error_messages={"invalid": "بودجه یا حقوق در نظر گرفته شده را وارد نمایید."},
        label="بودجه یا حقوق در نظر گرفته شده (ریال|توافقی)",
        widget=forms.TextInput(
                attrs={"class":"input-text", "placeholder":"1000000"}))

    category = forms.ModelChoiceField(
        label="دسته بندی",
        queryset=Category.objects.filter(status=True),
        widget=forms.Select(attrs={"class":"input-text"}))

    tags = SimpleArrayField(
        forms.CharField(max_length=100),
        label_suffix="تگ های پروژه(حداکثر 4 مورد)")

    work_type = forms.ChoiceField(
        label="نوع همکاری",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=WORK_TYPES)

    image = forms.FileField(
        label="عکس",
        required=False,
        allow_empty_file=True)

    description = QuillFormField(
        max_length=4000,
        label="توضیحات",
        error_messages={"required":"لطفا توضیحات پروژه را قرار دهید"})


    def clean_work_type(self):
        """
            Check whether the user has given a work type or not.
        """
        data = self.cleaned_data
        if data["work_type"] and data["work_type"] == "None":
            raise forms.ValidationError("لطفا نوع همکاری را مشخص نمایید")
        else:
            return data["work_type"]


    def clean_price(self):
        """
            Ensure the job price format is valid.
        """
        data = self.cleaned_data
        price = data["price"]

        if price.strip() == "توافقی":
            return price
        else:
            try:
                int_price = int(price)
                return price
            except ValueError:
                raise forms.ValidationError("لطفا هزینه پروژه را به ریال وارد نمایید یا از کلید واژه توافقی استفاده کنید")


class EditJobForm(forms.ModelForm, AddJobForm):
    
    class Meta:
        model = Job
        fields = AddJobForm().fields