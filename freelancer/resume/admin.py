from django.contrib import admin

from .models import CV, WorkExperience


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "gender", "marital_status")    
    list_display_links = ("user",)
    list_filter = ("gender", "marital_status")


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("cv", "position", "start_year", "end_year")
    list_display_links = ("cv",)
    list_filter = ("position", "start_year", "end_year")
