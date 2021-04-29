from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200, null=True) # not null
    priority = models.CharField(max_length=200, blank=True, null=True)
    duedate = models.DateField(auto_now=False)
    description = models.CharField(max_length=300, blank=True)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Day(models.Model):
    date = models.DateField()
    daily_tasks = models.ManyToManyField(Task)
    
    
class Profile(models.Model):
    fname=models.CharField(max_length=200, null=True,blank=True)
    lname=models.CharField(max_length=200, null=True,blank=True)
    headline=models.CharField(max_length=200, null=True,blank=True)
    position=models.CharField(max_length=200, null=True,blank=True)
    education=models.CharField(max_length=200, null=True,blank=True)
    country=models.CharField(max_length=200, null=True,blank=True)
    state=models.CharField(max_length=200, null=True,blank=True)
    image=models.ImageField(upload_to='profile_image', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
