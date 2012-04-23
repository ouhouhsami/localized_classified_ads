# coding=utf-8
from form_utils.forms import BetterModelForm
from moderation.forms import BaseModeratedObjectForm

from django import forms

from geoads.widgets import BooleanExtendedNumberInput
from utils.fields import PriceField, SurfaceField
from geoads.forms import BaseAdForm

from models import HomeForSaleAd


class HomeForSaleAdForm(BetterModelForm, BaseAdForm):

    price = PriceField(label="Prix (€)", help_text="Prix sans espace, sans virgule")
    surface = SurfaceField(label="Surface habitable (m²)", help_text="Surface, sans virgule")
    surface_carrez = SurfaceField(label="Surface Loi Carrez (m²)", required=False, help_text="Surface Loi Carrez, sans virgule")
    nb_of_rooms = forms.IntegerField(label="Nombre de pièces", error_messages={'required':'Ce champ est obligatoire.', 'invalid':'Entrez un nombre de pièce.'},)
    description = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'rows':7, 'cols':80}))
    balcony = forms.CharField(label="Balcon", required=False, widget=BooleanExtendedNumberInput(attrs={'label':"Balcon", 'detail':"préciser la surface (m²)"}))
    terrace = forms.CharField(label="Terrasse", required=False, widget=BooleanExtendedNumberInput(attrs={'label':"Terrasse", 'detail':"préciser la surface (m²)"}))
    separate_toilet = forms.CharField(label="Toilettes séparés", required=False, widget=BooleanExtendedNumberInput(attrs={'label':"Toilettes séparés", 'detail':"préciser leur nombre"}))
    bathroom = forms.CharField(label="Salle de bain", required=False, widget=BooleanExtendedNumberInput(attrs={'label':"Salle de bain", 'detail':"préciser leur nombre"}))
    shower = forms.CharField(label="Salle d'eau (douche)", required=False, widget=BooleanExtendedNumberInput(attrs={'label':"Salle d'eau (douche)", 'detail':"préciser leur nombre"}))



    def clean_balcony(self):
        data = self.cleaned_data['balcony']
        if data == '':
            data = None
        return data

    def clean_terrace(self):
        data = self.cleaned_data['terrace']
        if data == '':
            data = None
        return data

    def clean_separate_toilet(self):
        data = self.cleaned_data['separate_toilet']
        if data == '':
            data = None
        return data

    def clean_bathroom(self):
        data = self.cleaned_data['bathroom']
        if data == '':
            data = None
        return data

    def clean_shower(self):
        data = self.cleaned_data['shower']
        if data == '':
            data = None
        return data

    class Meta:
        model = HomeForSaleAd
        widgets = {
            'nb_of_bedrooms':forms.TextInput,
            'user_entered_address':forms.TextInput,
            'habitation_type':forms.Select
        }
        #TODO: line below could be "normally" removed, but need tests
        exclude = ('user', 'delete_date', 'location', 'address')
        fieldsets = [('title', {'fields': ['habitation_type', 'price', 'surface', 'surface_carrez', 'nb_of_rooms', 'nb_of_bedrooms','user_entered_address', 'ad_valorem_tax','housing_tax','maintenance_charges', 'energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Informations générales', 'classes':['house', 'apartment', 'parking', 'others', 'base']}),
                     ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain', 'classes':['house']}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'duplex', 'not_overlooked', 'orientation'], 'legend': 'Situation du logement dans l\'immeuble', 'classes': ['apartment']}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble', 'classes': ['apartment']}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'cellar', 'parking', 'alarm', 'balcony', 'terrace', 'fireplace', 'air_conditioning', 'swimming_pool'], 'legend': 'Commodités', 'classes': ['apartment', 'house', 'others']}),
                     ('rooms', {'fields' :['separate_dining_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces',  'classes': ['apartment', 'house', 'others']}),
                     #('storage_space', {'fields' :[], 'legend': 'Rangements'})
                     ('description', {'fields': ['description'], 'legend':'Informations complémentaires', 'classes':['house', 'apartment', 'parking', 'others']})
                     ]



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

    def nb_of_bedrooms(self):
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
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessiner votre propre zone de recherche cliquant sur la carte'}),
                     ('general_information', {'fields' : ['price','surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms'], 'classes':['visible']}),
                     ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'duplex', 'not_overlooked'], 'classes':[], 'legend': 'Situation'}),
                     ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble'}),
                     ('conveniences', {'fields' :['heating', 'kitchen', 'cellar', 'parking', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'terrace', 'balcony'], 'legend': 'Commodités'}),
                     ('rooms', {'fields' :['separate_dining_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance'], 'legend': 'Pièces'}),
                     ('energy', {'fields' :['energy_consumption', 'emission_of_greenhouse_gases'], 'legend': 'Critères énergétiques'}) ]        

