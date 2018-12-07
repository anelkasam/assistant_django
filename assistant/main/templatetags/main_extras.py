from datetime import date
from django import template

from todo.models import Category, Task

register = template.Library()


@register.simple_tag
def get_bootstrap_alert_msg_css_name(tags):
    """
    Edit error tag for the messages
    """
    return 'danger' if tags == 'error' else tags


@register.simple_tag
def get_today_task_number(user):
    """
    Return number of today tasks for the user
    """
    return Task.objects.filter(user=user,
                               status__in=[Task.NEW, Task.PROGRESS, Task.POSTPONE],
                               deadline__date=date.today()).count()


@register.inclusion_tag('cats.html')
def get_user_categories(user=None):
    """
    Return list of categories for the User. Just default categories if not user
    """
    return {'cats': Category.objects.filter(user=user, parent=None) if user.is_authenticated else [],
            'default': Category.objects.filter(user=None)}
