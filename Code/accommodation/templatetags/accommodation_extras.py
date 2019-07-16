from django import template

register = template.Library()


@register.simple_tag
def get_room_type(bed_type):
    if bed_type == 'Single':
        return 'اتاق سینگل'
    elif bed_type == 'Double':
        return 'اتاق دابل'
    else:
        return 'اتاق تویین'


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name
