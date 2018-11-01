from datetime import datetime
from django import forms
from django.db.models import Q

from .models import Category, Task, Files


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class DateInput(forms.DateInput):
    input_type = 'date'
    # attrs = {}


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(initial=datetime.now().strftime("%d-%m-%Y"),
                                   required=False, widget=DateInput())

    class Meta:
        model = Task
        fields = ['title', 'category', 'description', 'significance', 'deadline']

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(Q(user=user) | Q(user=None))


class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['title', 'upload']
