from django.urls import path,include

from . import views

app_name = "projects"

urlpatterns = [
    path('', views.index, name='index'),
    path('new/',views.project_new, name='project_new'),
    path('<int:project_id>/edit', views.project_edit, name='project_edit'),
    path('<int:project_id>/', views.detail, name='detail'), 
    path('stories/', include('projects.stories.urls', namespace='stories')),
    path('epics/',include('projects.epics.urls', namespace='epics')),
    path('delete/<int:project_id>/', views.delete, name='delete'),
]