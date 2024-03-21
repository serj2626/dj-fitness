from atexit import register
from posts.models import Category
from django import template


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()
