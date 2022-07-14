from django.contrib.admin import SimpleListFilter
from django.contrib import admin

from .models import ApplyProject, Project,  Category


class CategoryFilter(SimpleListFilter):
    """
       Filter by parent or children Category.
    """
    title = 'Category'
    parameter_name = 'category_type'

    def lookups(self, request, model_admin):
        return (('parent', 'Parent'),
                ("children", "Children"))

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        if self.value().lower() == 'children':
            verified_users = Category.objects.exclude(parent=None)
            return verified_users

        elif self.value().lower() == 'parent':
            unverified_users = Category.objects.filter(parent=None)
            return unverified_users


@admin.register(Category)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "status", "created")
    list_editable = ("status", )
    list_display_links = ("slug",)
    list_filter = ("status", CategoryFilter)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "urgent", "highlight", "private", "paid")
    list_editable = ("status", "urgent", "highlight", "private", "paid")
    list_display_links = ("title",)
    list_filter = ("status", "paid")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ApplyProject)
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "status")
    list_editable = ("status", )
    list_filter = ("status", )
    list_display_links = ("project",)