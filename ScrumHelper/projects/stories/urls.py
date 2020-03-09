from django.urls import path,include

from . import views

app_name = 'stories'

urlpatterns = [
    path('<int:story_id>/', views.detail, name='detail'),
    path('new/', views.story_new, name='story_new'),
]