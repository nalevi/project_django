from django.urls import path,include

from . import views

app_name = 'stories'

urlpatterns = [
    path('<int:story_id>/', views.detail, name='detail'),
    path('new/', views.story_new, name='story_new'),
    path('<int:story_id>/edit', views.story_edit, name='story_edit'),
    path('comment/<int:story_id>/', views.create_comment, name='create_comment')
]