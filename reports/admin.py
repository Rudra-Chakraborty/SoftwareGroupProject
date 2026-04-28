from django.contrib import admin
from .models import Department, Team, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'specialisation')
    search_fields = ('name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'manager', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'manager')
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role', 'email')
    search_fields = ('name',)
