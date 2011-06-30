# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
from form_utils.widgets import ImageWidget
from django.forms.extras.widgets import SelectDateWidget
from widgets import CustomPointWidget

class AdPictureForm(ModelForm):
    image = forms.ImageField(widget=ImageWidget(template='%(input)s<br /><div class="preview">%(image)s</div>'))
    #order = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = AdPicture

class AdContactForm(ModelForm):
    class Meta:
        model = AdContact
        exclude = ['user_profile', 'content_type', 'object_pk']

class HomeAdForm(BaseModeratedObjectForm, BetterModelForm):
    location = floppyforms.gis.PointField(widget = CustomPointWidget)

    #def __init__(self, *args, **kwargs):
    #    super(HomeForSaleAdForm, self).__init__(*args, **kwargs)
        #self.fields['location'] = floppyforms.gis.PointField(widget=CustomPointWidget(ads='self.qs'), label="Localisation")

    class Meta:
        exclude = ('user_profile', 'delete_date')
        fieldsets = [('title', {'fields': ['description', 'price', 'surface', 'habitation_type','nb_of_rooms', 'nb_of_bedrooms'], 'legend': 'L\'annonce'}),
                     ('location', {'fields': ['location'], 'legend': 'Localisation'}),
                     #('price', {'fields' :['price'], 'legend': 'Budget'}),
                     #('surface', {'fields' :['surface'], 'legend': 'Surface'}),
                     #('type', {'fields' :['habitation_type'], 'legend': 'Type d\'habitation'}),
                     #('pieces', {'fields' :['nb_of_rooms', 'nb_of_bedrooms'], 'legend': 'Pièces'}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'not_overlooked', 'orientation'], 'legend': 'Situation du logement dans l\'immeuble'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'duplex', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'parquet', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'living_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     ('storage_space', {'fields' :['cellar', 'cupboards', 'open_parking', 'box'], 'legend': 'Rangements'})]
    class Media:
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
        )


class HomeForSaleAdForm(HomeAdForm):
    #location = floppyforms.gis.PointField(widget = CustomPointWidget)

    #def __init__(self, *args, **kwargs):
    #    super(HomeForSaleAdForm, self).__init__(*args, **kwargs)
        #self.fields['location'] = floppyforms.gis.PointField(widget=CustomPointWidget(ads='self.qs'), label="Localisation")

    class Meta:
        model = HomeForSaleAd

class HomeForRentAdForm(HomeAdForm):
    #location = floppyforms.gis.PointField(widget = CustomPointWidget)

    #def __init__(self, *args, **kwargs):
    #    super(HomeForSaleAdForm, self).__init__(*args, **kwargs)
        #self.fields['location'] = floppyforms.gis.PointField(widget=CustomPointWidget(ads='self.qs'), label="Localisation")

    class Meta:
        model = HomeForRentAd

class HomeForSaleAdFilterSetForm(BetterModelForm):

    #def __init__(self, *args, **kwargs):
    #    super(HomeForSaleAdFilterSetForm, self).__init__(*args, **kwargs)
        #self['location'].value()


    # CLEAN def for each rangefield, multiplechoice field for validation purpose
    # Longtime bug to solve, cause of filterset link to a form, and form
    # not valid due to special filterfield
    # the thing not solved here is : why errors appear only if location field blank
    # and not if location field filled !
    def clean_price(self):
        pass

    def clean_surface(self):
        pass

    def clean_nb_of_rooms(self):
        pass

    def clean_ground_surface(self):
        pass

    def clean_floor(self):
        pass

    def clean_habitation_type(self):
        pass

    def clean_location(self):
        pass

    class Meta:
        model = HomeForSaleAd
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessinez votre zone de recherche sur la carte'}),
                     #, 'description':"Cliquez sur la carte pour dessiner le contour de votre zone de recherche, double-cliquez pour la fermer."
                     ('general_information', {'fields' : ['price','surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms']}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'not_overlooked', 'orientation'], 'legend': 'Situation'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'duplex', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'parquet', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'living_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     ('storage_space', {'fields' :['cellar', 'cupboards', 'open_parking', 'box'], 'legend': 'Rangements'})]        

    class Media:
        js = (
            '/static/js/map.utils.js',
        )


class HomeForRentAdFilterSetForm(HomeForSaleAdFilterSetForm):
    class Meta:
        model = HomeForRentAd
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessinez votre zone de recherche sur la carte'}),
                     #, 'description':"Cliquez sur la carte pour dessiner le contour de votre zone de recherche, double-cliquez pour la fermer."
                     ('general_information', {'fields' : ['price','surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms', 'colocation', 'furnished']}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'not_overlooked', 'orientation'], 'legend': 'Situation'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'duplex', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'parquet', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'living_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     ('storage_space', {'fields' :['cellar', 'cupboards', 'open_parking', 'box'], 'legend': 'Rangements'})]        
    