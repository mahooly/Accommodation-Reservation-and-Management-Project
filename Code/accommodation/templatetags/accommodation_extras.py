from django import template
from accommodation.models import Room

register = template.Library()


@register.simple_tag
def get_room_type(bed_type):
    if bed_type == 'Single':
        return 'اتاق سینگل'
    elif bed_type == 'Double':
        return 'اتاق دابل'
    else:
        return 'اتاق سینگل دو نفره'


@register.simple_tag
def divide_by_thousand(num):
    return num / 1000


@register.simple_tag
def get_room_price_from_id(room_id):
    print("idis ", room_id)
    return Room.objects.get(pk=room_id).price


@register.simple_tag
def get_room_price_from_id_2(room_id):
    print("idis ", room_id)
    return Room.objects.get(pk=room_id).price / 1000
