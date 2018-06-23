from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CookerProfile


# Register your models here.

class ProfileInLine(admin.StackedInline):
    """
    The admin form model to add custom fields from the CookerProfile
    """
    model = CookerProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInLine]


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
