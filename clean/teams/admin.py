from django.contrib import admin
from .models import Department, Team, TeamMember, TeamMessage, TeamMeeting

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'specialisation')
    search_fields = ('name', 'leader', 'specialisation')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'manager', 'is_active', 'created_at')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'manager', 'skills', 'contact_email')
    filter_horizontal = ('upstream_dependencies',)
    inlines = [TeamMemberInline]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role', 'email')
    search_fields = ('name', 'email', 'role')
    list_filter = ('team__department',)

@admin.register(TeamMessage)
class TeamMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'team', 'sender_name', 'sender_email', 'created_at')
    search_fields = ('subject', 'message', 'sender_name', 'sender_email')
    list_filter = ('team', 'created_at')

@admin.register(TeamMeeting)
class TeamMeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'organiser', 'date', 'start_time', 'platform')
    search_fields = ('title', 'team__name', 'organiser__username')
    list_filter = ('platform', 'date', 'team__department')
