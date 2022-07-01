from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_quill.forms import QuillFormField
from .models import Category


class AddJobForm(forms.Form):
    WORK_TYPES = (
            ('None', '---------'),
            ('full_time', 'تمام وقت'),
            ('part_time','پاره وقت'),
            ('teleworking','دور کاری'),
            ('internship','کاراموز'),
            ('temporary','موقت'))

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

    category = forms.ModelChoiceField(
        label="دسته بندی",
        queryset=Category.objects.filter(status=True),
        widget=forms.Select(attrs={"class":"input-text"}))

    price = forms.IntegerField(
        error_messages={"invalid": "لطفا عدد مورد نظر خود را به ریال وارد نمایید."},
        label="بودجه یه حقوق در نظر گرفته شده (ریال)",
        widget=forms.TextInput(
                attrs={"class":"input-text", "placeholder":"1000000"}))

    work_type = forms.ChoiceField(
        label="نوع همکاری",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=WORK_TYPES)

    tags = SimpleArrayField(
        forms.CharField(max_length=100),
        label_suffix="تگ های پروژه(حداکثر 4 مورد)")

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