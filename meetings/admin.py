# Author: Student 4
# Schedule
# Registers Meeting model in Django admin.

from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'team_name', 'date', 'start_time', 'end_time', 'platform', 'organiser']
    list_filter = ['platform', 'date']
    search_fields = ['title', 'team_name', 'organiser__username']
    ordering = ['date', 'start_time']
