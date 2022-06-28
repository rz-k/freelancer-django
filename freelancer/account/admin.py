from django.contrib import admin
from django.contrib.admin import SimpleListFilter, StackedInline

from .models import Profile, User


class UserProfileInline(StackedInline):
    model = Profile


class ApprovedUserFilter(SimpleListFilter):
    """
       Filter approved user.
    """
    title = 'Approved User'
    parameter_name = 'user_status'

    def lookups(self, request, model_admin):
        return (('approved', 'Approved'),
                ("unverified", "Unverified"))

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        
        if self.value().lower() == 'approved':
            verified_users = User.objects.filter(user_profile__approved=True)
            return verified_users
            
        elif self.value().lower() == 'unverified':
            unverified_users = User.objects.filter(user_profile__approved=False)
            return unverified_users


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, )    
    list_display = ("id", "email", "first_name", "last_name", "score", "is_verified")
    list_editable = ("first_name", "last_name","score")
    list_filter = (ApprovedUserFilter,)
    list_display_links = ("email",)

    
    def is_verified(self, record):
        user_profile = Profile.objects.filter(user=record).first()
        return user_profile.approved
    
    is_verified.boolean = True
