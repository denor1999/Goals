from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goals'
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Achievement(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    achieved_at = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'achievements'
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-achieved_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class GoalStep(models.Model):
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goal_steps'
        verbose_name = 'Шаг цели'
        verbose_name_plural = 'Шаги целей'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.goal.title}"
# Create your models here.
