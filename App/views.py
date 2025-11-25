from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Goal, GoalStep, Achievement
from .forms import GoalForm, GoalStepForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def index(request):
    goals = Goal.objects.filter(user=request.user)
    active_goals = goals.filter(is_completed=False)
    completed_goals = goals.filter(is_completed=True)

    message = request.GET.get('message', '')
    return render(request, 'index.html', {
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'message': message
    })


@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    message = request.GET.get('message', '')
    return render(request, 'goal_detail.html', {'goal': goal, 'message': message})


@login_required
def achievements(request):
    achievements_list = Achievement.objects.filter(user=request.user)
    completed_goals = Goal.objects.filter(user=request.user, is_completed=True)  # ← ТОЛЬКО выполненные!

    return render(request, 'achievements.html', {
        'achievements': achievements_list,
        'completed_goals': completed_goals
    })


@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f'Цель "{goal.title}" успешно создана!')
            return redirect('index')
    else:
        form = GoalForm()

    return render(request, 'add_goal.html', {'form': form})


@login_required
def add_step(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)

    if request.method == 'POST':
        form = GoalStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.goal = goal
            step.order = goal.steps.count() + 1
            step.save()
            messages.success(request, f'Шаг "{step.title}" добавлен!')
            return redirect('goal_detail', goal_id=goal.id)
    else:
        form = GoalStepForm()

    return render(request, 'add_step.html', {'form': form, 'goal': goal})


@login_required
def complete_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.is_completed = True
        goal.save()

        # Создаем достижение при завершении цели
        Achievement.objects.create(
            user=request.user,
            title=f'Завершена цель: {goal.title}',
            description=goal.description,
            points=100
        )

        messages.success(request, f'Цель "{goal.title}" успешно выполнена! 🎉')
        return redirect('goal_detail', goal_id=goal_id)
    return redirect('index')


@login_required
def reopen_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.is_completed = False
        goal.save()
        messages.success(request, f'Цель "{goal.title}" возвращена в работу!')
        return redirect('achievements')

    return redirect('index')


@login_required
def toggle_goal_status(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        if goal.is_completed:
            goal.is_completed = False
            message = 'Цель возвращена в работу!'
        else:
            goal.is_completed = True
            message = 'Цель отмечена как выполненная!'

            # Создаем достижение при завершении
            if goal.is_completed:
                Achievement.objects.create(
                    user=request.user,
                    title=f'Завершена цель: {goal.title}',
                    description=goal.description,
                    points=100
                )

        goal.save()
        messages.success(request, message)
        return redirect('index')
    return redirect('index')


@login_required
def toggle_step_status(request, goal_id, step_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        step = get_object_or_404(GoalStep, id=step_id, goal=goal)
        step.is_completed = not step.is_completed
        step.save()

        status = "выполнен" if step.is_completed else "возвращен в работу"
        messages.success(request, f'Шаг "{step.title}" {status}!')
        return redirect('goal_detail', goal_id=goal_id)
    return redirect('index')


@login_required
def delete_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal_title = goal.title
        goal.delete()
        messages.success(request, f'Цель "{goal_title}" удалена!')
        return redirect('index')

    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    return render(request, 'delete_goal.html', {'goal': goal})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('login')