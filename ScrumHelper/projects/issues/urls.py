from django.urls import path,include

from . import views

app_name = 'issues'

urlpatterns = [
    path('<int:issue_id>/', views.detail, name='detail'),
    path('new/', views.issue_new, name='issue_new'),
    path('<int:issue_id>/edit', views.issue_edit, name='issue_edit'),
    path('comment/<int:issue_id>/', views.create_comment, name='create_comment'),
    path('comment/delete/<int:issue_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('delete/<int:issue_id>/', views.delete, name='delete'),
    path('<int:issue_id>/change_state/', views.change_state, name='change_state'),
    path('<int:issue_id>/add_worklog/', views.add_worklog, name='add_worklog'),
]