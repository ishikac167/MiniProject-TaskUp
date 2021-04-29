from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from .models import *
from .forms import *
from .serializers import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from django.contrib.auth import login, authenticate

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def home(request):
    try:
        tasks = Task.objects.filter(user=request.user)
    except: # if no logged user
        class SignUpPage(generic.CreateView):
            form_class = UserCreationForm
            success_url = reverse_lazy('login')
            template_name = 'signup.html'
    days = Day.objects.all()
    today = Day.objects.get_or_create(date=datetime.date.today())[0]
    day=datetime.date.today()
    count=0
    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        if(task.done):
            count+=1
    # user_filter = UserFilter(request.GET, queryset=user)
    return render(request, "home_tasks.html", {"tasks":tasks, "days":days, "today":today, "count":count,"day":day})


def add_task(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        # title = request.POST.get("title")
        # priority = request.POST.get("priority")
        # duedate = request.POST.get("duedate")
        # description = request.POST.get("description")
        # # user = request.POST.get("user")
        # # done = request.POST.get("done")
        # add_task = TaskForm(title=title, priority=priority, duedate=duedate, description=description)
        # add_task.save()
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save_user(request)
    return redirect('/#tasks')     # Finally, redirect to the homepage.

def remove_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be removed
    if request.method == 'POST':         # If method is POST,
        task.delete()    
        return redirect('/#tasks')             # Finally, redirect to the homepage.     

def deleteAll(request):
    Task.objects.filter(user = request.user).delete()
    return redirect('/#tasks')

def task_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be removed
    if request.method == 'POST':         # If method is POST,
        if task.done:
            task.done = False
        else:
            task.done = True
        task.save(update_fields=["done"])
        return redirect('/#tasks')             # Finally, redirect to the homepage. 
   

def add_task_to_daily_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be added
    if request.method == 'POST':         # If method is POST,
        # add task to dayily tasks
        # the get_or_create method is that it actually returns a tuple of (object, created). 
        # The first element is an instance of the model you are trying to retrieve 
        # and the second is a boolean flag to tell if the instance was created or not. 
        # True means the instance was created by the get_or_create method and 
        # False means it was retrieved from the database.
        day = Day.objects.get_or_create(date=datetime.date.today())[0] 
        day.daily_tasks.add(task)
        day.save() # Django doesn’t hit the database until you explicitly call save().
        return redirect('/#tasks')             # Finally, redirect to the homepage.

def remove_task_from_daily_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be added
    if request.method == 'POST':         # If method is POST,
        # remove task from dayily tasks
        day = Day.objects.get(date=datetime.date.today())
        day.daily_tasks.remove(task)
        day.save() # Django doesn’t hit the database until you explicitly call save().
        return redirect('/#tasks')             # Finally, redirect to the homepage.

class TaskListView(LoginRequiredMixin, generic.ListView):
    """
    **Multiple inheritance**
    The generic view will query the database to get all records for 
    the specified model (Task) then render a template located at 
    templates/{tasks_app}/{task}_list.html
    """
    model = Task
    #queryset = Task.objects.filter(
    # =self.request.user)# Get tasks for that user
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class SignUpPage(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpPage(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('login')
#     else:
#         form = SignUpPage()
#         return render(request, 'signup.html', {'form': form})

# class LoginPage(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('home')
#     template_name = 'login.html'

def profile(request): 
    profile = Profile.objects.filter(user=request.user)
    
    # print(profile[len(profile)-1].fname)
    # user = User.objects.all()
    # user_filter = UserFilter(request.GET, queryset=user)
    


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
    count1=0
    count2=0
    count=0
    count3=0
    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        if(task.done):
            count1+=1
        if(task):
            count2+=1
        if(datetime.date.today() > task.duedate):
            count3+=1
    count=count2-count1-count3
    labels = 'Finished', 'Unfinished', 'Past Due'
    sizes = [count1, count, count3]
    colors = ['#000000', '#20b2aa', 'red']
    
    explode = (0.1, 0, 0) 
    fig1, ax1 = plt.subplots()
    patches, texts, autotexts=ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, colors=colors)
    for autotext in autotexts:
        autotext.set_color('white')        
    ax1.axis('equal')
    chart=plt.savefig('./tasks_app/static/sale_purchase_peichart.png',dpi=100)
    return render(request, "profile.html", {"profile":profile[len(profile)-1] if (len(profile)!=0) else profile})
    
    


def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save_user(request)
    return redirect('/profile')     # Finally, redirect to the profile.

class ProfileListView(LoginRequiredMixin, generic.ListView):
    """
    **Multiple inheritance**
    The generic view will query the database to get all records for 
    the specified model (Task) then render a template located at 
    templates/{tasks_app}/{task}_list.html
    """
    model = Profile
    #queryset = Task.objects.filter(
    # =self.request.user)# Get tasks for that user
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

def email(request):
    if request.method == "POST":
        name = request.POST.get['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            name,
            email,
            subject,
            message,
            ['ishikachokshi5@gmail.com']
        )
        return render(request,'/#contact',{'name':name,'email':email,'subject':subject,'message':message})
    else:
        return render(request,'/#contact',{})