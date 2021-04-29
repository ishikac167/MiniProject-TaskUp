from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.SignUpPage.as_view(), name='signup_page'),
    path('', views.home, name='home'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete/', views.deleteAll, name='delete'),
    path('<int:task_id>/remove_task/', views.remove_task, name='remove_task'),
    #path('<int:goal_id>/remove_goal/', views.remove_goal, name='remove_goal'),
    path('<int:task_id>/add_task_to_daily_tasks/', views.add_task_to_daily_tasks, name='add_task_to_daily_tasks'),
    path('<int:task_id>/remove_task_from_daily_tasks/', views.remove_task_from_daily_tasks, name='remove_task_from_daily_tasks'),
    #path('add_goal/', views.add_goal, name='add_goal'),
    path('<int:task_id>/task_done/', views.task_done, name='task_done'),
    #path('history/', views.history, name='history'),
    path('tasks_list/', views.TaskListView.as_view(), name='tasks_list'),
    path('signup_page/', views.SignUpPage.as_view(), name='signup_page'),
    path('email/', views.email, name='email'),
    #path('login/', views.LoginPage.as_view(), name='login')
    path('profile/', views.profile, name='profile'),
    path('profile/add_profile/', views.add_profile, name='add_profile'),
    path('profile_list/', views.ProfileListView.as_view(), name='profile_list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)