from django.contrib.admin import SimpleListFilter
from django.contrib import admin

from .models import ApplyProject, Project, Category, Conversation


class CategoryFilter(SimpleListFilter):
    """Filter category by parent or children."""
    title = "Category"
    parameter_name = "category_type"

    def lookups(self, request, model_admin):
        return (("parent", "Parent"), ("children", "Children"))

    def queryset(self, request, queryset):
        match self.value().__str__().lower():
            case "children":
                return Category.objects.exclude(parent=None)
            case "parent":
                return Category.objects.filter(parent=None)
            case _:
                return queryset


@admin.register(Category)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "name", "status", "created")
    list_editable = ("status", )
    list_display_links = ("slug",)
    list_filter = ("status", CategoryFilter)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "urgent",
                    "highlight", "private", "paid")
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


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "apply_project")
    list_display_links = ("apply_project", )
