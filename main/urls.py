from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]