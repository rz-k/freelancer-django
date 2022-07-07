from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import ApplyJob, Category, Job


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


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "salary")
    list_editable = ("salary", "status")
    list_display_links = ("title",)
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ApplyJob)
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "status")
    list_editable = ("status", )
    list_filter = ("status", )
    list_display_links = ("job",)
