# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
from django.forms.extras.widgets import SelectDateWidget

class GMapPointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    pass

class CustomPointWidget(GMapPointWidget):
    map_width = 500
    map_height = 400
    display_wkt = True

class UserProfileCustomForm(ModelForm):
    location = floppyforms.gis.PointField(widget = CustomPointWidget)
    birthdate = forms.DateField(widget=SelectDateWidget(), required = False)
    class Meta:
        model = UserProfile
        exclude = ('user',)
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )