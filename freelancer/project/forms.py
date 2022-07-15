from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django_quill.forms import QuillFormField
from freelancer.project.models import Category
from .models import Project


class AddProjectForm(forms.Form):
    title = forms.CharField(
        label_suffix="عنوان پروژه (کار)",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "input-text", "placeholder": "عنوان پروژه"}))

    category = forms.ModelChoiceField(
        label_suffix="دسته بندی",
        queryset=Category.objects.filter(status=True),
        widget=forms.Select(attrs={"class": "input-text"}))

    budget = forms.CharField(
        max_length=100,
        error_messages={"invalid": "بودجه  در نظر گرفته شده را وارد نمایید."},
        label_suffix="بودجه در نظر گرفته شده (ریال|توافقی)",
        widget=forms.TextInput(
            attrs={"class": "input-text", "placeholder": "1000000"}))

    tags = SimpleArrayField(
        label_suffix="تگ های پروژه(حداکثر 5 مورد)",
        base_field=forms.CharField(max_length=100))


    urgent = forms.BooleanField(
        label_suffix="این پروژه دارای تگ فوری باشد؟ (50 هزار تومان)",
        widget=forms.CheckboxInput(attrs={"class": "radio-check"}),
        required=False
        )


    highlight = forms.BooleanField(
        label_suffix="این پروژه دارای قالب رنگی متفاوتی باشد؟ (30 هزار تومان)",
        widget=forms.CheckboxInput(attrs={"class": "radio-check"}),
        required=False
        )


    private = forms.BooleanField(
        label_suffix="این پورژه فقط برای کاربران سایت نمایش داده شود؟ (20 هزار تومان)",
        widget=forms.CheckboxInput(attrs={"class": "radio-check"}),
        required=False
        )



    description = QuillFormField(
        max_length=10000,
        label_suffix="توضیحات",
        error_messages={"required": "لطفا توضیحات پروژه را قرار دهید"})

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
                raise forms.ValidationError(
                    "لطفا هزینه پروژه را به ریال وارد نمایید یا از کلید واژه توافقی استفاده کنید")


class EditProjectForm(forms.ModelForm, AddProjectForm):
    class Meta:
        model = Project
        fields = AddProjectForm().fields


class ApplyProjectForm(forms.Form):
    bid_amount = forms.IntegerField(
        label_suffix="مقدار پیشنهادی",
        widget=forms.TextInput(
            attrs={"class": "input-text", "placeholder": "برای مثال 220,500,000"}),
        error_messages={"bid_amount": "لطفا مقدار پیشنهادی پروژه را بنویسید"})

    bid_date = forms.IntegerField(
        min_value=1,
        label_suffix="زمان تحویل",
        widget=forms.TextInput(
            attrs={"class": "input-text"}),
        error_messages={"bid_date": "لطفا زمان تحویل پروژه را بنویسید"})

    description = forms.CharField(
        max_length=500,
        label_suffix="توضیحات",
        widget=forms.Textarea(
            attrs={"class": "input-text", "placeholder": "توضیحات..."}),
        error_messages={"required": "لطفا توضیحات خود را برای کارفرما بنویسید"})
