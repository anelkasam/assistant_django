from datetime import datetime
from django import forms
from django.db.models import Q

from .models import Category, Task, Files
from goals.models import Goal


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'parent']

    def __init__(self, user, *args, **kwargs):
        super(CreateCategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(Q(user=user) | Q(user=None))


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(initial=datetime.now().strftime("%d-%m-%Y"),
                                   required=False, widget=DateInput())

    class Meta:
        model = Task
        fields = ['title', 'category', 'goal', 'description', 'significance', 'status', 'deadline']

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(Q(user=user) | Q(user=None))
        self.fields['goal'].queryset = Goal.objects.filter(user=user)


class FileForm(forms.ModelForm):
    title = forms.CharField(required=False)
    upload = forms.FileField(required=False)

    class Meta:
        model = Files
        fields = ['title', 'upload']
