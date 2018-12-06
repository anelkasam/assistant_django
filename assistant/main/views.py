from datetime import date
from django.db.models import Q
from django.shortcuts import render

from todo.models import Task, Category
from goals.models import Goal


def index(request):
    context = {}
    if request.user.is_authenticated:
        tasks = Task.objects.select_related('category').filter(user=request.user,
                                    status__in=[Task.NEW, Task.PROGRESS, Task.POSTPONE]).order_by('category', '-status')
        goals = Goal.objects.filter(user=request.user,
                                    status__in=[Goal.NEW, Goal.PROGRESS])
        context = {
            'new_tasks_number': tasks.count(),
            'goals_number': goals.count()
        }
        tasks = tasks.filter(Q(deadline__date__lte=date.today()) | Q(deadline=None))
        categories = {cat: [] for cat in set(t.category.title for t in tasks)}
        for task in tasks:
            categories[task.category.title].append(task)
        context['categories'] = categories

    return render(request, 'index.html', context)
