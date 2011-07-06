# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
from django.forms.extras.widgets import SelectDateWidget
#from ads.widgets import CustomPointWidget

'''
class GMapPointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    pass

class CustomPointWidget(GMapPointWidget):
    map_width = 700
    map_height = 400
    #display_wkt = True
'''

class UserProfileCustomForm(ModelForm):
    #location = floppyforms.gis.PointField(widget = CustomPointWidget)
    class Meta:
        model = UserProfile
        exclude = ('user','mugshot', 'privacy')
