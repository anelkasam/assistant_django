from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from .forms import CreateCategoryForm, TaskForm, FileForm
from .models import Category, Task


class TaskList(ListView):
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(TaskList, self).get_context_data(*args, **kwargs)

        tasks = context['tasks']

        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            tasks = tasks.filter(category=category)

        sort_by = self.request.GET.get('sort', 'category')
        tasks = tasks.order_by(sort_by)
        active_tasks = tasks.filter(status__in=[Task.NEW, Task.PROGRESS, Task.POSTPONE])
        finished_tasks = tasks.filter(status__in=[Task.DONE, Task.CANCELED])

        cats = {}
        for t in active_tasks:
            cat = t.get_main_category().title
            cats[cat] = cats.get(cat, []) + [t]
        context['active_tasks'] = cats

        cats = {}
        for t in finished_tasks:
            cat = t.get_main_category().title
            cats[cat] = cats.get(cat, []) + [t]
        context['finished_tasks'] = cats

        return context


def create_task(request):
    """
    Create task view
    """
    category_form = CreateCategoryForm(request.user, prefix='category')
    if request.method == 'POST':
        task_form = TaskForm(request.user, request.POST, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.save()
            if request.FILES and file_form.is_valid():
                f = file_form.save(commit=False)
                f.content_object = task
                f.save()
            return redirect(request.POST.get('next', 'tasks'))
    else:
        task_form = TaskForm(request.user, prefix='task')
        file_form = FileForm(prefix='file')

    context = {'category_form': category_form,
               'task_form': task_form,
               'file_form': file_form}
    return render(request, 'add_task.html', context)


def create_category(request):
    if request.method == 'POST':
        category_form = CreateCategoryForm(request.user, request.POST, prefix='category')
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f'Category {category} was created.')
        return HttpResponseRedirect(request.POST.get('next', '/'))
    return HttpResponseNotAllowed(['POST'])


def edit_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    category_form = CreateCategoryForm(request.user, prefix='category')
    if request.method == 'POST':
        task_form = TaskForm(request.user, request.POST, instance=task, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')
        if task_form.is_valid():
            task_form.save()
            return redirect(reverse('tasks'))
    else:
        task_form = TaskForm(request.user, instance=task, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')

    return render(request, 'edit_task.html', {'task_form': task_form,
                                              'file_form': file_form,
                                              'category_form': category_form,
                                              'task': task})


def done_task(request, task_id):
    """
    Mark task as done
    """
    task = Task.objects.get(pk=task_id)
    task.status = Task.DONE
    task.save()
    return redirect(request.GET.get('next', reverse('tasks')))


def cancel_task(request, task_id):
    """
    Cancel task by id
    """
    task = Task.objects.get(pk=task_id)
    task.status = Task.CANCELED
    task.save()
    return redirect(request.GET.get('next', reverse('tasks')))
