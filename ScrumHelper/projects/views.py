from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Project
from .forms import CreateProjectForm

def index(request):
    projects_list = Project.objects.all()
    paginator = Paginator(projects_list, 5)

    page_number = request.GET.get('page',1)
    projects = paginator.get_page(page_number)

    context = {
        'project_list': projects_list,
        'projects': projects,
    }
    return render(request, 'projects/index.html', context)

def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/details.html', {'project': project})


def project_new(request):
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.project_owner = request.user
            proj.save()
            return redirect('projects:detail', project_id=proj.id )
    else:
        form = CreateProjectForm()
    return render(request, 'projects/project_edit.html', {'form': form})

