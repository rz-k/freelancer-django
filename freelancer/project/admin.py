from django.contrib import admin

from .models import ApplyProject, Project


@admin.register(Project)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "urgent", "highlight", "private", "paid")
    list_editable = ("status", "urgent", "highlight", "private", "paid")
    list_display_links = ("title",)
    list_filter = ("status", "paid")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(ApplyProject)