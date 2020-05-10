from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name='index'),
    path('team_worklogs/', views.team_worklogs, name='team_worklogs'),
    path('all_users/', views.list_all_users, name='list_all_users'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:gr_id>', views.group_detail, name='group_detail'),
    path('groups_delete/<int:gr_id>', views.delete_group, name='delete_group'),
    path('add_permission/<int:gr_id>/<int:p_id>', views.add_perm_to_group, name='add_perm_to_group'),
    path('delete_permission/<int:gr_id>/<int:p_id>', views.delete_perm_from_group, name='delete_perm_from_group'),
    path('<username>/', views.detail, name='detail'),
    path('delete_user/<int:user_id>',views.delete_user, name='delete_user'),
    path('<username>/worklogs/', views.get_users_worklogs, name='get_users_worklogs'),
    path('delete_worklog/<int:log_id>', views.delete_worklog, name='delete_worklog'),
    path('delete_from_group/<int:user_id>/<int:group_id>', views.delete_from_group, name='delete_from_group'),
]