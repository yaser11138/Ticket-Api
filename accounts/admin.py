from django.contrib import admin
from .models import MyUser
# Register your models h


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    pass