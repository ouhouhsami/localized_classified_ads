# coding=utf-8
from django import template
#from django.forms import ChoiceField, FileField

register = template.Library()


@register.filter(name='email_local_part')
def email_local_part(mail):
    return mail.split('@')[0].replace('.', ' ')

'''
@register.filter(name='field_value')
def field_value(field):
	""" 
	Returns the value for this BoundField, as rendered in widgets. 
	""" 
	if field.form.is_bound: 
		if isinstance(field.field, FileField) and field.data is None: 
			val = field.form.initial.get(field.name, field.field.initial) 
		else: 
			val = field.data 
	else:
		val = field.form.initial.get(field.name, field.field.initial)
		if callable(val):
			val = val()
	if val is None:
		val = ''
	return val


@register.filter(name='display_value')
def display_value(field): 
	""" 
	Returns the displayed value for this BoundField, as rendered in widgets. 
	""" 
	value = field_value(field)
	if isinstance(field.field, ChoiceField): 
		for (val, desc) in field.field.choices: 
			if val == value: 
				return desc 
	return value
	

@register.filter(name='widget_type')
def widget_type(ob):
    return ob.__class__.__name__
'''

