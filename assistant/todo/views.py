from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from .forms import CreateCategoryForm, TaskForm, FileForm
from .models import Category, Task, DEFAULT_CATEGORY


def pack_tasks_by_category(user, tasks):
    cats = {cat.id: (cat, []) for cat in Category.objects.filter(user=user, parent=None)}
    cats[DEFAULT_CATEGORY] = (Category.objects.get(pk=DEFAULT_CATEGORY), [])
    for t in tasks:
        cat = t.get_main_category()
        cats[cat.id][1].append(t)
    return cats.values()


class TaskList(ListView):
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(TaskList, self).get_context_data(*args, **kwargs)

        context['category_form'] = CreateCategoryForm(self.request.user, prefix='category')

        tasks = context['tasks']
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            tasks = tasks.filter(category=category)

        tasks = tasks.order_by(self.request.GET.get('sort', 'category'))
        active_tasks = tasks.filter(status__in=[Task.NEW, Task.PROGRESS, Task.POSTPONE])
        finished_tasks = tasks.filter(status__in=[Task.DONE, Task.CANCELED])
        context['active_tasks'] = pack_tasks_by_category(self.request.user, active_tasks)
        context['finished_tasks'] = pack_tasks_by_category(self.request.user, finished_tasks)

        return context


def create_task(request):
    """
    Create task view
    """
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

    context = {'task_form': task_form,
               'file_form': file_form}
    return render(request, 'add_task.html', context)


def create_category(request):
    """
    Form is in modal window that is why this view calls only for POST method
    """
    if request.method == 'POST':
        category_form = CreateCategoryForm(request.user, request.POST, prefix='category')
        if category_form.is_valid():
            category_form.save()
            messages.success(request, f'Category {category} was created.')
        return redirect(reverse('tasks'))
    return HttpResponseNotAllowed(['POST'])


def edit_category(request, cat_id):
    category = Category.objects.get(pk=cat_id)
    if request.method == 'POST':
        category_form = CreateCategoryForm(request.user, request.POST,
                                           instance=category, prefix='category')
        if category_form.is_valid():
            category_form.save()
            messages.success(request, f'Category {category} was updated.')
            return redirect(reverse('tasks'))
    else:
        category_form = CreateCategoryForm(request.user, instance=category, prefix='category')
    return render(request, 'edit_category.html', {'category_form': category_form,
                                                  'category': category})


def edit_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task_form = TaskForm(request.user, request.POST, instance=task, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')
        if task_form.is_valid():
            task_form.save()
            return redirect(request.POST.get('next', reverse('tasks')))
    else:
        task_form = TaskForm(request.user, instance=task, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')

    return render(request, 'edit_task.html', {'task_form': task_form,
                                              'file_form': file_form,
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
