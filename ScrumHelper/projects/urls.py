from django.urls import path,include

from . import views

app_name = "projects"

urlpatterns = [
    path('', views.index, name='index'),
    
]