from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from goals.models import Goal


DEFAULT_CATEGORY = 1


class Category(models.Model):
    """
    Category for the tasks
    """
    title = models.CharField('Category title', max_length=40)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name='Own to user')

    class Meta:
        unique_together = (("title", "user"),)

    def delete(self, *args, **kwargs):
        """
        Deprecate deletion of the Default category
        """
        if self.id == DEFAULT_CATEGORY:
            raise Exception('You cannot delete this Category')
        super(Category, self).delete(*args, **kwargs)

    @property
    def get_category_tree(self):
        """
        Return string representation of this category with all its parents
        'parent/sub1/sub2/self'
        """
        cat = self
        cats = [cat.title]
        while cat.parent is not None:
            cat = cat.parent
            cats.insert(0, cat.title)

        return '/'.join(cats)

    @property
    def is_leaf(self):
        """
        Returns True if category don't have children, False otherwise
        """
        return self.category_set.all().count() == 0

    def get_all_children(self):
        """Returns all child categories"""
        children = [self]
        nodes = [self]
        while nodes:
            node = nodes.pop()
            cats = list(node.category_set.all())
            children = children + cats
            for cat in cats:
                if cat.is_leaf:
                    continue
                nodes.append(cat)

        return children

    def __str__(self):
        return self.title


class Files(models.Model):
    """
    Files that can be connected to the Task or other models
    """
    title = models.CharField('Title', max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    upload = models.FileField('File', upload_to='uploads/')


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='User')
    status = models.IntegerField('Status', choices=STATUSES, default=0)
    significance = models.IntegerField('Significance', choices=SIGNIFICANCE, default=0)
    files = GenericRelation(Files)
    goal = models.ForeignKey(Goal, null=True, blank=True, default=None,
                             on_delete=models.CASCADE, verbose_name='For goal')

    def delete(self, *args, **kwargs):
        self.status = self.CANCELED
        self.save()

    def get_main_category(self):
        """
        Returns the main category for the task
        """
        if not self.category.parent:
            return self.category

        cat = self.category.parent
        while cat.parent:
            cat = cat.parent
        return cat

    def __str__(self):
        return f'{self.title} ({self.category}). Due to {self.deadline}'
