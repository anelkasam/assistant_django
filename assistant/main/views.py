from datetime import date
from django.db.models import Q
from django.shortcuts import render

from todo.models import Task
from goals.models import Goal


def index(request):
    context = {}
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user,
                                    status__in=[Task.NEW, Task.PROGRESS, Task.POSTPONE])
        goals = Goal.objects.filter(user=request.user,
                                    status__in=[Goal.NEW, Goal.PROGRESS])
        context = {'today_tasks': tasks.filter(Q(deadline__date__lte=date.today()) | Q(deadline=None )),
                   'new_tasks_number': tasks.count(),
                   'goals_number': goals.count()}
    return render(request, 'index.html', context)
