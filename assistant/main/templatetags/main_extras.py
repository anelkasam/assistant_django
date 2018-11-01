from django import template

from todo.models import Category

register = template.Library()


@register.simple_tag
def get_bootstrap_alert_msg_css_name(tags):
    """
    Edit error tag for the messages
    """
    return 'danger' if tags == 'error' else tags


@register.inclusion_tag('cats.html')
def get_user_categories(user=None):
    """
    Return list of categories for the User. Just default categories if not user
    """
    return {'cats': Category.objects.filter(user=user),
            'default': Category.objects.filter(user=None)}
