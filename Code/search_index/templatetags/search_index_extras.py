from django import template

register = template.Library()


@register.filter
def get_url(value, url):
    return '/accommodation/' + str(value) + url
