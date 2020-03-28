from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

from .models import Project, Documents
from .forms import CreateProjectForm
from .services import get_issues_for_project, delete_project

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
   
    context = get_issues_for_project(project_id)
    

    return render(request, 'projects/details.html', context)


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

def project_edit(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = CreateProjectForm(request.POST, instance=proj)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.save()
            return redirect('projects:detail', project_id=proj.id )
    else:
        form = CreateProjectForm(instance=proj)
    return render(request, 'projects/project_edit.html', {'form': form})

def delete(request, project_id):
    success = delete_project(project_id=project_id)

    if success:
        return redirect('projects:index')

def upload_doc(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        if 'documentation' in request.FILES:
            uploaded_file = request.FILES['documentation']

            doc = Documents()
            doc.document.save(uploaded_file.name, uploaded_file)
            project.documents.add(doc)

    return redirect('projects:detail', project_id=project_id )
