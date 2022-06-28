import imp
from django.contrib import admin
from django.contrib.admin import StackedInline
from .models import User, Profile



class UserProfileInline(StackedInline):
    model = Profile

@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, ]
    list_display = ["user_id","email","first_name", "last_name", "score", "user_approved"]
    list_editable = ("first_name","last_name","score",)

    def user_approved(self, record):
        prf = Profile.objects.filter(user=record).first()
        return prf.approved

    def user_id(self, record):
        return record.id

    # @admin.action(description="make approved true")
    # def MakeApprovedTrue(self, request, queryset):
    #     print(queryset)
    #     # prf = Profile.objects.filter(user=record).first()
    #     rows = queryset.update(available=True)
    #     # self.message_user(request, f"{rows} Product is Avaleble Success !")