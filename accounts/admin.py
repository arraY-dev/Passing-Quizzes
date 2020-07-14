from django.contrib import admin
from django.contrib.auth.models import User

from . import models


class ResultUserAdmin(admin.TabularInline):
    model = models.PassedUserQuiz


class UserAdmin(admin.ModelAdmin):
    inlines = [ResultUserAdmin, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Profile)
admin.site.register(models.Answer)
admin.site.register(models.Question)
admin.site.register(models.Quiz)
admin.site.register(models.Comment)
admin.site.register(models.PassedUserQuiz)
