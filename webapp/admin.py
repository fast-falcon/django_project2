from django.contrib import admin

# Register your models here.

from webapp.models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('bio','gender','picture')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Teacher Free Times"
    list_display = ('start', 'end', 'date', 'teacher', 'capacity')
