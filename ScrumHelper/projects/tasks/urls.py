from django.urls import path,include

from . import views

app_name = 'tasks'

urlpatterns = [
    path('<int:task_id>/', views.detail, name='detail'),
    path('new/', views.task_new, name='task_new'),
    path('<int:task_id>/edit', views.task_edit, name='task_edit'),
    path('comment/<int:task_id>/', views.create_comment, name='create_comment'),
    path('comment/delete/<int:task_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('delete/<int:task_id>/', views.delete, name='delete'),
    path('<int:task_id>/change_state/', views.change_state, name='change_state'),
    path('<int:task_id>/add_worklog/', views.add_worklog, name='add_worklog'),
]