from django.urls import path
from . import views

urlpatterns = [

    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("departments/", views.department_view, name="departments"),


    path("messages/", views.inbox, name="inbox"),
    path("messages/outbox/", views.outbox, name="outbox"),
    path("messages/compose/", views.compose, name="compose"),
]
