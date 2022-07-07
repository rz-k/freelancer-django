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

    MILITARY_SERVICE_STATUS_CHOICES  = (
        ('no_matter','مهم نیست'),
        ('end_Soldeir','پایان خدمت',),
        ('soldier','سرباز'),
        ('exempt','معافیت'),
    )

    EDUCATIONAL_LEVEL_CHOICES  = (
        ('no_matter','مهم نیست',),
        ('diploma','دیپلم'),
        ('lisanse','لیسانس'),
        ('mastersdegree','فوق لیسانس'),
        ('phd','دکترا و بالاتر'),
    )

    GENDER_CHOICES  = (
        ('no_matter','مهم نیست'),
        ('man','اقا'),
        ('femail','خانوم'),

    )
    category = forms.ModelChoiceField(
        label="دسته بندی",
        queryset=Category.objects.filter(status=True),
        widget=forms.Select(attrs={"class":"input-text"}))

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

    tags = SimpleArrayField(
        forms.CharField(max_length=100),
        label_suffix="تگ های پروژه(حداکثر 10 مورد)")


    description = QuillFormField(
        max_length=20000,
        label="توضیحات",
        error_messages={"required":"لطفا توضیحات پروژه را قرار دهید"})

    place = forms.CharField(
        label="موقعیت مکانی",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class":"input-text", "placeholder":"تهران , تهران"}))


    work_type = forms.ChoiceField(
        label="نوع همکاری",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=WORK_TYPES)


    image = forms.FileField(
        label="عکس",
        required=False,
        allow_empty_file=True)


    experience = forms.CharField(
        required=False,
        label="سابقه کار(تعداد سال)",
        widget=forms.TextInput(
            attrs={"class":"input-text", "placeholder":"بین 2 تا 3 سال"}))

    salary = forms.CharField(
        max_length=100,
        error_messages={"invalid": "بودجه یا حقوق در نظر گرفته شده را وارد نمایید."},
        label="بودجه یا حقوق در نظر گرفته شده (ریال|توافقی)",
        widget=forms.TextInput(
                attrs={"class":"input-text", "placeholder":"1000000"}))

    gender = forms.ChoiceField(
        label="جنسیت",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=GENDER_CHOICES)


    military_status = forms.ChoiceField(
        label="نظام وظیفه",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=MILITARY_SERVICE_STATUS_CHOICES)   


    educational_level = forms.ChoiceField(
        label="مدرک تحصیلی",
        widget=forms.Select(attrs={"class":"input-text"}),
        choices=EDUCATIONAL_LEVEL_CHOICES)   

    urgent = forms.BooleanField()
    highlight = forms.BooleanField()
    private = forms.BooleanField()



    def clean_work_type(self):
        """
            Check whether the user has given a work type or not.
        """
        data = self.cleaned_data
        if data["work_type"] and data["work_type"] == "None":
            raise forms.ValidationError("لطفا نوع همکاری را مشخص نمایید")
        else:
            return data["work_type"]


    def clean_salary(self):
        """
            Ensure the job salary format is valid.
        """
        data = self.cleaned_data
        salary = data["salary"]

        if salary.strip() == "توافقی":
            return salary
        else:
            try:
                int_price = int(salary)
                return salary
            except ValueError:
                raise forms.ValidationError("لطفا حقوق پیشنهادی را به ریال وارد نمایید یا از کلید واژه توافقی استفاده کنید")



class EditJobForm(forms.ModelForm, AddJobForm):

    class Meta:
        model = Job
        fields = AddJobForm().fields


class ApplyForm(forms.Form):
    bid_amount = forms.IntegerField(
        label="مقدار پیشنهادی",
        widget=forms.TextInput(
            attrs={"class":"input-text", "placeholder": "برای مثال 220,500,000"}),
        error_messages={"bid_amount":"لطفا مقدار پیشنهادی پروژه را بنویسید"})

    bid_date = forms.IntegerField(
        min_value=1,
        label="زمان تحویل",
        widget=forms.TextInput(
            attrs={"class":"input-text"}),
        error_messages={"bid_date":"لطفا زمان تحویل پروژه را بنویسید"})

    description = forms.CharField(
        max_length=500,
        label="توضیحات",
        widget=forms.Textarea(
                attrs={"class": "input-text", "placeholder": "توضیحات..."}),
        error_messages={"required": "لطفا توضیحات خود را برای کارفرما بنویسید"})