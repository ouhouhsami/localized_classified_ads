# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
from django.forms.extras.widgets import SelectDateWidget


class UserProfileCustomForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','mugshot', 'privacy')
