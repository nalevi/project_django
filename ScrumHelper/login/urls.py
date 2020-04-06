from django.urls import path,include

from . import views
from .views import CustomLoginView


app_name = 'login'

urlpatterns = [ 
    path('', CustomLoginView.as_view()),
    path('registration/signup/', views.signup, name='signup'),
    path('edit_user/<username>', views.edit_user, name='edit_user'),
    path('', include('django.contrib.auth.urls')),
]