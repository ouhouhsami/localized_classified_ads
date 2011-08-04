# coding=utf-8
from django import forms
from django.contrib.gis.geos import Point, Polygon
from django.forms import ModelForm
from moderation.forms import BaseModeratedObjectForm
from models import *
import floppyforms
from form_utils.forms import BetterModelForm, BetterForm
#from form_utils.widgets import ImageWidget
from django.forms.extras.widgets import SelectDateWidget
from widgets import CustomPointWidget
from django.utils.safestring import mark_safe


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
            #image_html = thumbnail(value.name, self.width, self.height)
            #print value.thumbnail.url()
            output = self.template % {'input': input_html, 'image': value.url,
                                      'image_thumbnail': value.thumbnail.url()}
        else:
            output = input_html
        return mark_safe(output)

class AdPictureForm(ModelForm):
    image = forms.ImageField(widget=ImageWidget())
    #order = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = AdPicture

class AdContactForm(ModelForm):
    class Meta:
        model = AdContact
        exclude = ['user_profile', 'content_type', 'object_pk']

class HomeAdForm(BaseModeratedObjectForm, BetterModelForm):
    location = floppyforms.gis.PointField(widget = CustomPointWidget)
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'rows':7, 'cols':150}))
    #def __init__(self, *args, **kwargs):
    #    super(HomeForSaleAdForm, self).__init__(*args, **kwargs)
        #self.fields['location'] = floppyforms.gis.PointField(widget=CustomPointWidget(ads='self.qs'), label="Localisation")

    class Meta:
        exclude = ('user_profile', 'delete_date')
        fieldsets = [('title', {'fields': ['price', 'surface', 'habitation_type','nb_of_rooms', 'nb_of_bedrooms', 'location', 'energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Informations générales (obligatoires)'}),
                     #('location', {'fields': ['location'], 'legend': 'Localisation', 'description': '<b>Cliquez sur la carte pour localiser votre bien.</b>'}),
                     #('location', {'fields': ['location'], 'description': '', 'legend': ''}),
                     #('price', {'fields' :['price'], 'legend': 'Budget'}),
                     #('surface', {'fields' :['surface'], 'legend': 'Surface'}),
                     #('type', {'fields' :['habitation_type'], 'legend': 'Type d\'habitation'}),
                     #('pieces', {'fields' :['nb_of_rooms', 'nb_of_bedrooms'], 'legend': 'Pièces'}),
                     #('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'duplex', 'not_overlooked', 'orientation'], 'legend': 'Situation du logement dans l\'immeuble'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'cellar', 'parking', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     #('storage_space', {'fields' :[], 'legend': 'Rangements'})
                     ('description', {'fields': ['description'], 'legend':'Informations complémentaires'})
                     ]
        #row_attrs = {'description': {'cols': '150', 'rows':'7'}}
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
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessiner votre zone de recherche en cliquant sur la carte'}),
                     #, 'description':"Cliquez sur la carte pour dessiner le contour de votre zone de recherche, double-cliquez pour la fermer."
                     ('general_information', {'fields' : ['price','surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms']}),
                     #('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'duplex', 'not_overlooked', 'orientation'], 'legend': 'Situation'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'cellar', 'parking', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     #('storage_space', {'fields' :['cellar', 'parking'], 'legend': 'Rangements'}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ]        

    class Media:
        js = (
            '/static/js/map.utils.js',
        )


class HomeForRentAdFilterSetForm(HomeForSaleAdFilterSetForm):
    class Meta:
        model = HomeForRentAd
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessiner votre zone de recherche en cliquant sur la carte'}),
                     #, 'description':"Cliquez sur la carte pour dessiner le contour de votre zone de recherche, double-cliquez pour la fermer."
                     ('general_information', {'fields' : ['price','surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms', 'colocation', 'furnished']}),
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain'}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'duplex', 'not_overlooked', 'orientation'], 'legend': 'Situation'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'cellar', 'parking', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     #('storage_space', {'fields' :['cellar', 'parking'], 'legend': 'Rangements'}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ,
                     ]        
    