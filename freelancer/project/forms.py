from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_quill.forms import QuillFormField
from freelancer.job.models import Category
from .models import Project


class AddProjectForm(forms.Form):

    title = forms.CharField(
        label="عنوان پروژه (کار)",
        max_length=100,
        widget=forms.TextInput(            
            attrs={"class":"input-text", "placeholder":"عنوان پروژه یا شغل"}))
    
    
    category = forms.ModelChoiceField(
        label="دسته بندی",
        queryset=Category.objects.filter(status=True),
        widget=forms.Select(attrs={"class":"input-text"}))

    tags = SimpleArrayField(
        forms.CharField(max_length=100),
        label_suffix="تگ های پروژه(حداکثر 5 مورد)")
    
    description = QuillFormField(
        max_length=10000,
        label="توضیحات",
        error_messages={"required":"لطفا توضیحات پروژه را قرار دهید"})

    budget = forms.CharField(
        max_length=100,
        error_messages={"invalid": "بودجه  در نظر گرفته شده را وارد نمایید."},
        label="بودجه در نظر گرفته شده (ریال|توافقی)",
        widget=forms.TextInput(
                attrs={"class":"input-text", "placeholder":"1000000"}))


    urgent = forms.BooleanField()
    highlight = forms.BooleanField()
    private = forms.BooleanField()


    def clean_budget(self):
        """
            Ensure the project budget format is valid.
        """
        data = self.cleaned_data
        budget = data["budget"]

        if budget.strip() == "توافقی":
            return budget
        else:
            try:
                int_price = int(budget)
                return budget
            except ValueError:
                raise forms.ValidationError("لطفا هزینه پروژه را به ریال وارد نمایید یا از کلید واژه توافقی استفاده کنید")


class EditProjectForm(forms.ModelForm, AddProjectForm):
    class Meta:
        model = Project
        fields = AddProjectForm().fields


class ApplyProjectForm(forms.Form):
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