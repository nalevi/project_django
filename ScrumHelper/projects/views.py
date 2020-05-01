from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from datetime import datetime, timedelta

from .stories.models import UserStory
from .tasks.models import Task
from .issues.models import Issue
from .models import Project, Documents
from .forms import CreateProjectForm
from .services import get_issues_for_project, delete_project

def index(request):
    projects_list = Project.objects.all().order_by('-created_date')
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

def delete_doc(request, project_id,doc_id):
    project = Project.objects.get(pk=project_id)

    document = project.documents.get(id=doc_id).delete()
    return redirect('projects:detail', project_id=project_id)


def kanban_board(request):
    stories = UserStory.objects.all()
    tasks = Task.objects.all()
    issues = Issue.objects.all()
    
    
    open_stories = stories.filter(state="OPEN")
    open_tasks = tasks.filter(state="OPEN")
    open_issues = issues.filter(state="OPEN")

    inprogress_stories = stories.filter(state="IN PROGRESS")
    inprogress_tasks = tasks.filter(state="IN PROGRESS")
    inprogress_issues = issues.filter(state="IN PROGRESS")

    testing_stories = stories.filter(state="TESTING")
    testing_tasks = tasks.filter(state="TESTING")
    testing_issues = issues.filter(state="TESTING")

    done_stories = stories.filter(state="DONE").filter(modified_date__gt=datetime.today()-timedelta(days=30))
    done_tasks = tasks.filter(state="DONE").filter(modified_date__gt=datetime.today()-timedelta(days=30))
    done_issues = issues.filter(state="DONE").filter(modified_date__gt=datetime.today()-timedelta(days=30))

    context = {
        'open_stories': open_stories,
        'inprogress_stories': inprogress_stories,
        'testing_stories': testing_stories,
        'done_stories': done_stories,
        'open_tasks': open_tasks,
        'inprogress_tasks': inprogress_tasks,
        'testing_tasks': testing_tasks,
        'done_tasks': done_tasks,
        'open_issues': open_issues,
        'inprogress_issues': inprogress_issues,
        'testing_issues': testing_issues,
        'done_issues': done_issues,
    }

    return render(request, 'projects/kanban.html', context)


def get_chart_data(request):
    stories = UserStory.objects.all()
    tasks = Task.objects.all()
    issues = Issue.objects.all()
    
    
    open_stories = stories.filter(state="OPEN").count()
    open_tasks = tasks.filter(state="OPEN").count()
    open_issues = issues.filter(state="OPEN").count()

    inprogress_stories = stories.filter(state="IN PROGRESS").count()
    inprogress_tasks = tasks.filter(state="IN PROGRESS").count()
    inprogress_issues = issues.filter(state="IN PROGRESS").count()

    testing_stories = stories.filter(state="TESTING").count()
    testing_tasks = tasks.filter(state="TESTING").count()
    testing_issues = issues.filter(state="TESTING").count()

    done_stories = stories.filter(state="DONE").count()
    done_tasks = tasks.filter(state="DONE").count()
    done_issues = issues.filter(state="DONE").count()

    json = {
        'open_all': open_stories + open_tasks + open_issues,
        'inprogress_all': inprogress_stories + inprogress_tasks + inprogress_issues,
        'testing_all': testing_stories + testing_tasks + testing_issues, 
        'done_all': done_stories + done_tasks + done_issues,
    }

    # JsonResponse(json)
    return render(request, 'projects/kanban_chart.html', json)