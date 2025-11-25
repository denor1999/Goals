from django import forms
from .models import Goal, GoalStep

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'target_date']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Опишите вашу цель...'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название цели'}),
        }
        labels = {
            'title': 'Название цели',
            'description': 'Описание',
            'target_date': 'Дата выполнения',
        }

class GoalStepForm(forms.ModelForm):
    class Meta:
        model = GoalStep
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название шага'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Описание шага (необязательно)'}),
        }