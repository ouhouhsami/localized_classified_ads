# coding=utf-8
from django import forms
from django.utils.translation import ugettext as _


class SpecificRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.TextInput(attrs={'placeholder':'min'}), 
                   forms.TextInput(attrs={'placeholder':'max'}))
        super(SpecificRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u' - '.join(rendered_widgets)


indifferent_choices = ((u'1', _('Indifferent')),
                       (u'2', _('Yes')),
                       (u'3', _('No')))
