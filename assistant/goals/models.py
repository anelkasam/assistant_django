from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    NEW = 0
    PROGRESS = 1
    POSTPONE = 2
    ARCHIVED = 3
    CANCELED = 4
    STATUSES = (
        (NEW, 'New'),
        (PROGRESS, 'In progress'),
        (POSTPONE, 'Postpone'),
        (ARCHIVED, 'Archived'),
        (CANCELED, 'Canceled')
    )
    title = models.CharField('Title', max_length=120)
    description = models.TextField('Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='User')
    status = models.IntegerField('Status', choices=STATUSES, default=NEW)
    parent = models.ForeignKey('Goal', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Goal: {self.title}'
