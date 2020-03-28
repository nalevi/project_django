from django.urls import path,include

from . import views

app_name = 'stories'

urlpatterns = [
    path('<int:story_id>/', views.detail, name='detail'),
    path('new/', views.story_new, name='story_new'),
    path('<int:story_id>/edit', views.story_edit, name='story_edit'),
    path('comment/<int:story_id>/', views.create_comment, name='create_comment'),
    path('comment/delete/<int:story_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('delete/<int:story_id>/', views.delete, name='delete'),
    path('<int:story_id>/change_state/', views.change_state, name='change_state'),
]