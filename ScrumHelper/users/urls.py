from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name='index'),
    path('team_worklogs/', views.team_worklogs, name='team_worklogs'),
    path('<username>/', views.detail, name='detail'),
    path('<username>/worklogs/', views.get_users_worklogs, name='get_users_worklogs'),
    path('delete_worklog/<int:log_id>', views.delete_worklog, name='delete_worklog'),
]