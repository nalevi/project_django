from django.urls import path,include

from . import views

app_name = "projects"

urlpatterns = [
    path('', views.index, name='index'),
    path('new/',views.project_new, name='project_new'),
    path('<int:project_id>/', views.detail, name='detail'),  
]