from django import template

register = template.Library()

@register.filter
def to_slesh(value):
    return value.replace("_"," ").capitalize()

@register.filter
def from_slesh(value):
    return value.replace(" ","_").capitalize()