from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('goal/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('achievements/', views.achievements, name='achievements'),
    path('goal/<int:goal_id>/complete/', views.complete_goal, name='complete_goal'),
    path('goal/<int:goal_id>/reopen/', views.reopen_goal, name='reopen_goal'),
    path('goal/<int:goal_id>/toggle/', views.toggle_goal_status, name='toggle_goal_status'),
]