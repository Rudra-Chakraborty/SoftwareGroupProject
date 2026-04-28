# Author: Student 4
# Schedule
# URL routing for the schedule app.

from django.urls import path
from . import views
app_name = 'schedule'
urlpatterns = [
    path('', views.upcoming_view, name='upcoming'),
    path('monthly/', views.monthly_view, name='monthly'),
    path('weekly/', views.weekly_view, name='weekly'),
    path('new/', views.create_meeting, name='create'),
    path('<int:pk>/', views.meeting_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_meeting, name='edit'),
    path('<int:pk>/delete/', views.delete_meeting, name='delete'),
]
