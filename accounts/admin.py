from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser
# Register your models h


@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
    pass