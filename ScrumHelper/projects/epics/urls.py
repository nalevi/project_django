from django.urls import path,include

from . import views

app_name = 'epics'

urlpatterns = [
    path('<int:epic_id>/', views.detail, name='detail'),
    path('new/', views.epic_new, name='epic_new'),
    path('<int:epic_id>/edit', views.epic_edit, name='epic_edit'),
    path('delete/<int:epic_id>/', views.delete, name='delete')
]