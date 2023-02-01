from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Announcement)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(Newsletter)
admin.site.register(UserProfile)
