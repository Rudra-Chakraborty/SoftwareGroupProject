from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Uploaded group-project pages
    path('', main_views.login_view, name='login'),
    path('dashboard/', main_views.dashboard, name='dashboard'),
    path('admin-dashboard/', main_views.admin_dashboard, name='admin_dashboard'),
    path('profile/', main_views.profile_view, name='profile'),

    # Student 1 pages
    path('teams/', include(('teams.urls', 'teams'))),
    path('departments/', team_views.department_list, name='departments'),
    path('departments/<int:pk>/', team_views.department_detail, name='department_detail'),
    path('dependencies/', team_views.dependency_list, name='dependencies'),
    path('schedule/', include('meetings.urls', namespace='schedule')),
    path('reports/', include('reports.urls', namespace='reports')),
]
