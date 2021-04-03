from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .forms import *

# rest_framework
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.
def index(request):
    date = dt.date.today()
    heading = "Welcome to Nicholas Awward Application"
    projects = Projects.objects.all()
    
    return render(request, 'home.html', {"date": date, "heading":heading, "projects":projects})


def get_project_by_id(request, id):

    try:
        project = Projects.objects.get(pk = id)
        
    except ObjectDoesNotExist:
        raise Http404()    
    
    return render(request, "project.html", {"project":project})


@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = current_user
            project.save()
        return redirect('index')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form":form})