from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from auth_extension.models import Profile


DEFAULT_CATEGORY = 1


class Category(models.Model):
    title = models.CharField('Category title', max_length=40)
    profile = models.ForeignKey(Profile, null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name='Own to user')

    class Meta:
        unique_together = (("title", "profile"),)

    def delete(self, *args, **kwargs):
        if self.id != 1:
            super(Category, self).delete(*args, **kwargs)
        # ToDo: in other case send exception

    def __str__(self):
        return self.title


class Files(models.Model):
    title = models.CharField('Title', max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    upload = models.FileField('File', upload_to='uploads/')

    def __str__(self):
        return self.title


class Task(models.Model):
    NEW = 0
    PROGRESS = 1
    POSTPONE = 2
    DONE = 3
    CANCELED = 4
    STATUSES = (
        (NEW, 'New'),
        (PROGRESS, 'In progress'),
        (POSTPONE, 'Postpone'),
        (DONE, 'Done'),
        (CANCELED, 'Canceled')
    )
    UI = 0
    UnI = 1
    nUI = 2
    nUnI = 3
    SIGNIFICANCE = (
        (UI, 'Urgent and important'),
        (UnI, 'Urgent and not important'),
        (nUI, 'Not urgent and important'),
        (nUnI, 'Not urgent and not important')
    )

    title = models.CharField('Title', max_length=120)
    description = models.TextField('Description', null=True, blank=True)
    category = models.ForeignKey(Category, default=DEFAULT_CATEGORY, on_delete=models.SET_DEFAULT)
    deadline = models.DateTimeField('Deadline', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='User')
    status = models.IntegerField('Status', choices=STATUSES, default=0)
    significance = models.IntegerField('Significance', choices=SIGNIFICANCE, default=0)
    files = GenericRelation(Files)

    def delete(self, *args, **kwargs):
        self.status = self.CANCELED

    def __str__(self):
        return f'{self.title} ({self.category}). Due to {self.deadline}'
