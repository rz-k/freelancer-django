from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_quill.forms import QuillFormField
from .models import Category


class AddJobForm(forms.Form):
    WORK_TYPES = (
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
        label="بودجه یه حقوق در نظر گرفته شده (ریال)",
        # max_value=1000000,
        widget=forms.TextInput(
                attrs={"class":"input-text", "placeholder":"1000000"}))

    work_type = forms.ChoiceField(
        label="نوع همکاری",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=WORK_TYPES)

    tags = SimpleArrayField(
        forms.CharField(max_length=100),
        label_suffix="تگ های پروژه(حداکثر 4 مورد)")
    
    image = forms.FileField(required=False, label="عکس" ,allow_empty_file=True)    
    description = QuillFormField(label="توضیحات", max_length=4000)
    