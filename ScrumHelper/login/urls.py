from django.urls import path,include

from .views import CustomLoginView

app_name = 'login'

urlpatterns = [ 
    path('', CustomLoginView.as_view()),
    path('', include('django.contrib.auth.urls')),
]