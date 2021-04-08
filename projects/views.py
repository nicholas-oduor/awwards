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

class ProjectsList(APIView):
    def get(self, request, format=None):
        all_merch = Projects.objects.all()
        serializers = ProjectsSerializer(all_merch, many=True)
        return Response(serializers.data)
    
class ProjectsDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_projects(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return Http404
        
    def get(self, request, pk, format=None):
        project = self.get_projects(pk)
        serializers = ProjectsSerializer(project)
        return Response(serializers.data)
    
    def put(self, request, pk, format=None):
        project = self.get_projects(pk)
        serializers = ProjectsSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        project = self.get_projects(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileList(APIView):
    def get(self, request, format=None):
        all_merch = Profile.objects.all()
        serializers = ProfileSerializer(all_merch, many=True)
        return Response(serializers.data)
    
@login_required(login_url='/accounts/login/')
def search_projects(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_projects = Projects.search_projects(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})
    
@login_required(login_url='/accounts/login/')
def user_profiles(request):
    current_user = request.user
    author = current_user
    projects = Projects.get_by_author(author)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('profile')
        
    else:
        form = ProfileUpdateForm()    
    return render(request, 'django_registration/profile.html', {"form":form, "projects":projects})
