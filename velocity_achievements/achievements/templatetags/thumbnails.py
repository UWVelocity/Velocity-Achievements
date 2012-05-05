from django import template

register = template.Library()

@register.inclusion_tag('render.html')
def thumbnail(tag,width,height):
    return {'render':tag.thumbnail(width,height)}
