from django.urls import path,include

from . import views
from .views import CustomLoginView


app_name = 'login'

urlpatterns = [ 
    path('', CustomLoginView.as_view()),
    path('registration/signup/', views.signup, name='signup'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('change_pw/<int:user_id>', views.change_pw, name='change_pw'),
    path('', include('django.contrib.auth.urls')),
]