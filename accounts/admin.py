from django.contrib import admin
from django.contrib.auth.models import User

from . import models
from tests.models import PassedUserQuiz


class ResultUserAdmin(admin.TabularInline):
    model = PassedUserQuiz


class UserAdmin(admin.ModelAdmin):
    inlines = [ResultUserAdmin, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Profile)

