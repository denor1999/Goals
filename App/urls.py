from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('goal/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('goal/add/', views.add_goal, name='add_goal'),
    path('goal/<int:goal_id>/add-step/', views.add_step, name='add_step'),
    path('goal/<int:goal_id>/complete/', views.complete_goal, name='complete_goal'),
    path('goal/<int:goal_id>/reopen/', views.reopen_goal, name='reopen_goal'),
    path('goal/<int:goal_id>/toggle/', views.toggle_goal_status, name='toggle_goal_status'),
    path('goal/<int:goal_id>/step/<int:step_id>/toggle/', views.toggle_step_status, name='toggle_step_status'),
    path('goal/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),
    path('achievements/', views.achievements, name='achievements'),
]