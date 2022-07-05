from django.contrib import admin
from django.contrib.admin import SimpleListFilter, StackedInline
from .models import CV, WorkExperience, Education, Contact


class WorkExperienceInline(StackedInline):
    model = WorkExperience

class EducationInline(StackedInline):
    model = Education

class ContactInline(StackedInline):
    model = Contact




@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    inlines = (WorkExperienceInline,EducationInline, ContactInline) 
    list_display = ("user", "country", "gender", "marital_status")    
    list_display_links = ("user",)
    list_filter = ("gender", "marital_status")

