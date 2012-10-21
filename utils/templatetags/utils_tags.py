#-*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='email_local_part')
def email_local_part(mail):
    return mail.split('@')[0].replace('.', ' ')
