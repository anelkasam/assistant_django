from django.db import models
from ckeditor.fields import RichTextField
from goals.models import Goal
from todo.models import Task


class Note(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()
    task = models.ForeignKey(Task,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='To task')
    goal = models.ForeignKey(Goal,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='To goal')

    def __str__(self):
        return f'[Note] {self.title}'


class Link(models.Model):
    title = models.CharField(max_length=200)
    body = models.URLField()
    task = models.ForeignKey(Task,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='To task')
    goal = models.ForeignKey(Goal,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             verbose_name='To goal')

    def __str__(self):
        return f'[Link] {self.title}'
