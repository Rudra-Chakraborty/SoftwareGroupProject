from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('pdf/', views.generate_pdf, name='generate_pdf'),
    path('excel/', views.generate_excel, name='generate_excel'),
    path('chart-data/', views.chart_data, name='chart_data'),
]
