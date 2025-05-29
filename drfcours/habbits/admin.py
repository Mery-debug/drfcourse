from django.contrib import admin

from .models import Habits


@admin.register(Habits)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "move")