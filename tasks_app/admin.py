from django.contrib import admin
from .models import Task,Day,Profile
# Register your models here.
admin.site.register([Task, Day,Profile])
