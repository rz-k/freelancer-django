from django.contrib import admin
from django.contrib.admin import SimpleListFilter, StackedInline

from .models import Profile, User


class UserProfileInline(StackedInline):
    model = Profile


class ApprovedUserFilter(SimpleListFilter):
    """Filter approved user."""
    title = "Approved User"
    parameter_name = "user_status"

    def lookups(self, request, model_admin):
        return (("approved", "Approved"), ("unapproved", "UnApproved"))

    def queryset(self, request, queryset):
        match self.value().__str__().lower():
            case "approved":
                return User.objects.filter(profile__approved=True)
            case "unapproved":
                return User.objects.filter(profile__approved=False)
            case _:
                return queryset


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, )
    list_display = ("id", "email", "first_name",
                    "last_name", "score", "is_approved")
    list_editable = ("first_name", "last_name", "score")
    list_filter = (ApprovedUserFilter,)
    list_display_links = ("email",)

    def is_approved(self, record):
        user_profile = Profile.objects.filter(user=record).first()
        return user_profile.approved

    is_approved.boolean = True
