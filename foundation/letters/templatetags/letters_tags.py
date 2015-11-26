from __future__ import absolute_import
from django import template
from foundation.letters.utils import can_send
register = template.Library()


@register.assignment_tag
def user_can_send(user, case):
    return can_send(user, case)
