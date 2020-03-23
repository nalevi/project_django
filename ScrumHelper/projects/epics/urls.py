from django.urls import path,include

from . import views

app_name = 'epics'

urlpatterns = [
    path('<int:epic_id>/', views.detail, name='detail'),
    path('new/', views.epic_new, name='epic_new'),
    #path('<int:story_id>/edit', views.story_edit, name='story_edit'),
    #path('delete/<int:story_id>/', views.delete, name='delete')
]