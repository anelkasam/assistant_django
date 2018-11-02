from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView

from .forms import CreateCategoryForm, TaskForm, FileForm
from .models import Category, Task, Goal


class TaskList(ListView):
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            return Task.objects.filter(user=self.request.user, category=category).order_by('status')
        return Task.objects.filter(user=self.request.user).order_by('status')


@login_required
def create_task(request):
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
            return redirect('tasks')
    else:
        task_form = TaskForm(request.user, prefix='task')
        file_form = FileForm(prefix='file')

    context = {'task_form': task_form, 'file_form': file_form}
    return render(request, 'add_task.html', context)


@login_required
def create_category(request):
    if request.method == 'POST':
        category = Category.objects.create(title=request.POST['title'], user=request.user)
        messages.success(request, f'Category {category} was created.')
        return redirect('add_task')
    return HttpResponseNotAllowed(['POST'])


@login_required
def edit_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task_form = TaskForm(request.user, request.POST, instance=task, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')
        if task_form.is_valid():
            task_form.save()
            return redirect('tasks')
    else:
        task_form = TaskForm(request.user, instance=task, prefix='task')
        file_form = FileForm(request.POST, request.FILES, prefix='file')

    return render(request, 'edit_task.html', {'task_form': task_form,
                                              'file_form': file_form,
                                              'task': task})

