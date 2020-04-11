from django.urls import path,include

from . import views

app_name = "projects"

urlpatterns = [
    path('', views.index, name='index'),
    path('new/',views.project_new, name='project_new'),
    path('<int:project_id>/edit', views.project_edit, name='project_edit'),
    path('<int:project_id>/upload_doc', views.upload_doc, name='upload_doc'),
    path('<int:project_id>/delete_doc/<int:doc_id>', views.delete_doc, name='delete_doc'),
    path('<int:project_id>/', views.detail, name='detail'), 
    path('stories/', include('projects.stories.urls', namespace='stories')),
    path('epics/',include('projects.epics.urls', namespace='epics')),
    path('tasks/', include('projects.tasks.urls', namespace='tasks')),
    path('issues/', include('projects.issues.urls', namespace='issues')),
    path('delete/<int:project_id>/', views.delete, name='delete'),
    path('kanban/', views.kanban_board, name='kanban_board'),
    path('kanban_chart/', views.get_chart_data, name='get_chart_data'),
]