from django import template

register = template.Library()

@register.simple_tag
def my_tostring(arg1):
    """concatenate arg1 & arg2"""
    return str(arg1)

@register.simple_tag
def get_full_name(feed):
    return feed.get_full_name()

@register.simple_tag
def get_username(feed):
    return feed.get_username()

@register.simple_tag
def get_commentator_name(comment):
    return comment.owner.get_full_name()