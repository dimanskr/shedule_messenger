import datetime
from django import template

register = template.Library()

# фильтр вывода полного пути к изображению
@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"
