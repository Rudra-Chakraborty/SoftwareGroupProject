from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('dependencies/', views.dependency_list, name='dependencies'),
    path('', views.team_list, name='list'),
    path('meetings/', views.my_team_meetings, name='meetings'),
    path('departments/', views.department_list, name='departments'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('<int:pk>/', views.team_detail, name='detail'),
    path('<int:pk>/email/', views.email_team, name='email'),
    path('<int:pk>/schedule/', views.schedule_team_meeting, name='schedule'),
]
