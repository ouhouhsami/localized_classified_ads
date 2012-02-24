# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
from django.forms.extras.widgets import SelectDateWidget
from widgets import CustomPointWidget, BooleanExtendedNumberInput
from django.utils.safestring import mark_safe

from fields import PriceField, SurfaceField

class ImageWidget(forms.FileInput):
    template = '%(input)s<br /><a href="%(image)s" target="_blank"><img src="%(image_thumbnail)s" /></a>'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        input_html = super(forms.FileInput, self).render(name, value, attrs)
        if hasattr(value, 'width') and hasattr(value, 'height'):
            output = self.template % {'input': input_html, 'image': value.url,
                                      'image_thumbnail': value.thumbnail.url()}
        else:
            output = input_html
        return mark_safe(output)

class AdPictureForm(ModelForm):
    image = forms.ImageField(widget=ImageWidget(), required=False)
    class Meta:
        model = AdPicture

class AdContactForm(ModelForm):
    class Meta:
        model = AdContact
        exclude = ['user_profile', 'content_type', 'object_pk']



