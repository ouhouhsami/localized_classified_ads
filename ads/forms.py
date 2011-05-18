# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
from django.forms.extras.widgets import SelectDateWidget
from widgets import CustomPointWidget


class HomeForSaleAdForm(BaseModeratedObjectForm, BetterModelForm):
    location = floppyforms.gis.PointField(widget = CustomPointWidget)

    def __init__(self, *args, **kwargs):
        super(HomeForSaleAdForm, self).__init__(*args, **kwargs)
        #self.fields['location'] = floppyforms.gis.PointField(widget=CustomPointWidget(ads='self.qs'), label="Localisation")

    class Meta:
        model = HomeForSaleAd
        exclude = ('user_profile', 'delete_date')
        fieldsets = [('title', {'fields': ['title', 'description'], 'legend': 'L\'annonce'}),
                     ('location', {'fields': ['location'], 'legend': 'Localisation'}),
                     ('price', {'fields' :['price'], 'legend': 'Budget'}),
                     ('surface', {'fields' :['surface'], 'legend': 'Surface'}),
                     ('type', {'fields' :['habitation_type'], 'legend': 'Type d\'habitation'}),
                     ('pieces', {'fields' :['nb_of_rooms', 'nb_of_bedrooms'], 'legend': 'Pièces'}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'top_floor', 'orientation'], 'legend': 'Situation du logement dans l\'immeuble'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'duplex', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'parquet', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'living_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     ('storage_space', {'fields' :['cellar', 'cupboards', 'open_parking', 'box'], 'legend': 'Rangements'})]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )

class HomeForSaleAdFilterSetForm(BetterModelForm):

    def __init__(self, *args, **kwargs):
        super(HomeForSaleAdFilterSetForm, self).__init__(*args, **kwargs)
        #self['location'].value()

    class Meta:
        model = HomeForSaleAd
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessinez votre zone de recherche', 'description':"Sur la carte ci-dessous, cliquez pour ajouter un point, double-cliquez pour fermer la zone de recherche."}),
                     ('general_information', {'fields' : ['price','surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms']}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'top_floor', 'orientation'], 'legend': 'Le logement dans l\'immeuble'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'duplex', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'parquet', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'living_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     ('storage_space', {'fields' :['cellar', 'cupboards', 'open_parking', 'box'], 'legend': 'Rangements'})]        

    class Media:
        js = (
            '/static/js/map.utils.js',
        )

class AdContactForm(ModelForm):
    class Meta:
        model = AdContact
        exclude = ['user_profile', 'content_type', 'object_pk']


    