from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Статические данные целей
GOALS_DATA = [
    {
        'id': 1,
        'title': 'Изучить Python',
        'description': 'Освоить основы языка Python и научиться писать простые программы',
        'deadline': '2024-12-31',
        'status': 'in_progress',
        'steps': [
            'Пройти онлайн-курс по Python',
            'Решить 50 задач на CodeWars',
            'Создать небольшой проект',
            'Изучить основы ООП в Python'
        ]
    },
    {
        'id': 2,
        'title': 'Научиться играть на гитаре',
        'description': 'Освоить базовые аккорды и сыграть 3 простые песни',
        'deadline': '2024-08-15',
        'status': 'in_progress',
        'steps': [
            'Купить гитару',
            'Найти преподавателя или онлайн-курс',
            'Выучить базовые аккорды (Am, C, G, D, E)',
            'Научиться играть бой и перебор',
            'Сыграть первую песню полностью'
        ]
    },
    {
        'id': 3,
        'title': 'Прочитать 12 книг за год',
        'description': 'Регулярно читать художественную и профессиональную литературу',
        'deadline': '2024-12-31',
        'status': 'completed',
        'steps': [
            'Составить список книг для чтения',
            'Выделять 30 минут на чтение каждый день',
            'Вести читательский дневник',
            'Делиться впечатлениями в книжном клубе'
        ]
    },
    {
        'id': 4,
        'title': 'Научиться готовить 5 новых блюд',
        'description': 'Расширить кулинарные навыки, освоив новые рецепты',
        'deadline': '2024-06-30',
        'status': 'completed',
        'steps': [
            'Выбрать 5 интересных рецептов',
            'Составить список продуктов',
            'Приготовить каждое блюдо минимум 2 раза',
            'Угостить друзей или семью'
        ]
    }
]


def get_goal_by_id(goal_id):
    return next((g for g in GOALS_DATA if g['id'] == goal_id), None)


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
    goals = GOALS_DATA
    message = request.GET.get('message', '')
    return render(request, 'index.html', {'goals': goals, 'message': message})

@login_required
def goal_detail(request, goal_id):
    goal = get_goal_by_id(int(goal_id))
    message = request.GET.get('message', '')
    return render(request, 'goal_detail.html', {'goal': goal, 'message': message})

@login_required
def achievements(request):
    completed_goals = [g for g in GOALS_DATA if g['status'] == 'completed']
    return render(request, 'achievements.html', {'goals': completed_goals})

@login_required
def complete_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_goal_by_id(int(goal_id))
        if goal:
            goal['status'] = 'completed'
            return redirect(f'/goal/{goal_id}/?message=Цель успешно выполнена! 🎉')
    return redirect('index')

@login_required
def reopen_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_goal_by_id(int(goal_id))
        if goal:
            goal['status'] = 'in_progress'
            return redirect(f'/goal/{goal_id}/?message=Цель возвращена в работу!')
    return redirect('index')

@login_required
def toggle_goal_status(request, goal_id):
    if request.method == 'POST':
        goal = get_goal_by_id(int(goal_id))
        if goal:
            if goal['status'] == 'in_progress':
                goal['status'] = 'completed'
                message = 'Цель отмечена как выполненная!'
            else:
                goal['status'] = 'in_progress'
                message = 'Цель возвращена в работу!'

            return redirect(f'/?message={message}')
    return redirect('index')

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('login')