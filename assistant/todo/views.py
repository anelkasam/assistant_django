from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView

from .forms import CreateCategoryForm, TaskForm, FileForm
from .models import Category, Task, Goal


class TaskList(ListView):
    template_name = 'task_list.html'
    ordering = 'deadline'
    context_object_name = 'tasks'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            return Task.objects.filter(user=self.request.user, category=category)
        return Task.objects.filter(user=self.request.user)


@login_required
def create_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.user, request.POST)
        file_form = FileForm(request.POST, request.FILES)
    else:
        task_form = TaskForm(request.user)
        file_form = FileForm()

    return render(request, 'add_task.html', {
        'task_form': task_form,
        'file_form': file_form
    })
