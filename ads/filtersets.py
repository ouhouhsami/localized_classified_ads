# coding=utf-8
import django_filters
from django_filters.filters import Filter
from django_filters.widgets import RangeWidget
from django import forms
from django.forms import widgets
from filters import LocationFilter, BooleanForNumberFilter
from widgets import PolygonWidget, IndifferentNullBooleanSelect, GooglePolygonWidget
from django.utils.translation import ugettext as _

class SpecificRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.TextInput(attrs={'placeholder':'min'}), forms.TextInput(attrs={'placeholder':'max'}))
        super(SpecificRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u' - '.join(rendered_widgets)


indifferent_choices = ((u'1', _('Indifferent')),(u'2', _('Yes')),(u'3', _('No')))
