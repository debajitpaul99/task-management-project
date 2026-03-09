from django import template

register = template.Library()

@register.filter(name='group')
def group(user, group_name):
    return user.groups.filter(name=group_name).exists()
