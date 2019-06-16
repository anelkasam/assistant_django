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
        cats = {}
        for t in tasks:
            cat = t.get_main_category().title
            cats[cat] = cats.get(cat, []) + [t]
        context['categories'] = cats

    return render(request, 'index.html', context)
