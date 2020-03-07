from django.shortcuts import render

from .models import Project

def index(request):
    projects_list = Project.objects.all()
    context = {
        'project_list': projects_list,
    }
    return render(request, 'projects/index.html', context)
