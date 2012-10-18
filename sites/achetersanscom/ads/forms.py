# coding=utf-8
import logging
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML
from crispy_forms.bootstrap import AppendedText, Field

from django import forms


from geoads.widgets import BooleanExtendedNumberInput

from utils.fields import PriceField, SurfaceField
from utils.bootstrap import MultiField, BootstrapFieldset

from models import HomeForSaleAd
from utils.forms import BaseModeratedAdForm

import floppyforms as forms

logger = logging.getLogger(__name__)


class HomeForSaleAdForm(BaseModeratedAdForm):

    price = PriceField(
        label="Prix",
        help_text="Prix sans espace, sans virgule"
    )

    surface = SurfaceField(
        label="Surface habitable",
        help_text="Surface, sans virgule"
    )

    surface_carrez = SurfaceField(
        label="Surface Loi Carrez",
        required=False,  # why do I need this to false, model no false ?
        help_text="Surface Loi Carrez, sans virgule"
    )

    nb_of_rooms = forms.IntegerField(
        label="Nombre de pièces", 
        error_messages={'required': 'Ce champ est obligatoire.', 
                        'invalid':'Entrez un nombre de pièce.'},
    )

    description = forms.CharField(
        label="Description", 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 7, 'cols': 80})
    )

    balcony = forms.CharField(
        label="", 
        required=False, 
        widget=BooleanExtendedNumberInput(attrs={'label': "Balcon",
                              'detail': "préciser la surface (m²)"})
    )

    terrace = forms.CharField(
        label="", 
        required=False, 
        widget=BooleanExtendedNumberInput(attrs={'label': "Terrasse",
                              'detail': "préciser la surface (m²)"}))

    separate_toilet = forms.CharField(
        label="", 
        required=False, 
        widget=BooleanExtendedNumberInput(attrs={'label':"Toilettes séparés",
                                           'detail':"préciser leur nombre"}))

    bathroom = forms.CharField(
        label="", 
        required=False, 
        widget=BooleanExtendedNumberInput(attrs={'label':"Salle de bain", 
                                            'detail':"préciser leur nombre"}))

    shower = forms.CharField(
        label="", 
        required=False, 
        widget=BooleanExtendedNumberInput(attrs={'label':"Salle d'eau (douche)",
                                                'detail':"préciser leur nombre"})
    )

    # clean functions
    # ugly, this is due to bad widget code

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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(u'Informations générales',
                      'habitation_type', AppendedText('price', '€', css_class="input-mini"), 
                      AppendedText('surface', 'm²', css_class="input-mini"), 
                      AppendedText('surface_carrez', 'm²', css_class="input-mini"), 
                      'nb_of_rooms', 'nb_of_bedrooms','user_entered_address', 
                      AppendedText('ad_valorem_tax', '€/an', css_class="input-mini"),
                      AppendedText('housing_tax', '€/an', css_class="input-mini"),
                      AppendedText('maintenance_charges', '€/an', css_class="input-mini"), 
                      'energy_consumption', 'emission_of_greenhouse_gases',
                      css_class = "atom house apartment parking others base"
            ),
            Fieldset(u'Surface du terrain', 'ground_surface',
                      css_class = "atom house"
            ),
            Fieldset(u'Situation du logement dans l\'immeuble', 'floor',
                      MultiField('', 'ground_floor',
                                  'top_floor', 'duplex', 'not_overlooked',
                                  css_class='control-group', label_class='control-label'),
                      'orientation',
                      css_class = "atom apartment"
            ),
            Fieldset(u'A propos de l\'immeuble',
                      MultiField('', 'elevator', 'intercom',
                      'digicode', 'doorman'),
                      css_class = "atom apartment"
            ),
            Fieldset(u'Commodités', 'heating', MultiField('', 'kitchen', 'cellar'),
                      'parking', MultiField('', 'alarm', 'balcony', 'terrace'), 'fireplace',
                      MultiField('', 'air_conditioning', 'swimming_pool'),
                      css_class = "atom apartment house others"
            ),
            Fieldset(u'Pièces', MultiField('', 'separate_dining_room', 'separate_toilet',
                      'bathroom', 'shower', 'separate_entrance'),
                      css_class = "atom apartment house others"
            ),
            Fieldset(u'Informations complémentaires', Field('description',  template="crispy_forms/no_label_field.html", css_class="input-xxlarge"),
                       css_class = "atom house apartment parking others", css_id="description"),
            Div(
                Submit('submit', "Enregister l'annonce", css_class="btn btn-large btn-block btn-primary", style="width:100%")
            ),
        )

        super(HomeForSaleAdForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeForSaleAd
        widgets = {
            'nb_of_bedrooms': forms.TextInput,
            'user_entered_address': forms.TextInput,
            'habitation_type': forms.Select
        }
        #TODO: line below could be "normally" removed, but need tests
        #logger.debug('class Meta of HomeForSaleAdForm')
        exclude = ('user', 'delete_date', 'location', 'address', 'visible')


class HomeForSaleAdFilterSetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'get'
        self.helper.form_action = '.'
        self.helper.form_tag = False
        self.helper.layout = Div(
                Div(
                    Div(
                        Field('location', css_id="location", template='bootstrap/map.html'),
                        HTML('{% include "geoads/search_results.html" %}'),
                        css_id="maps", name="maps", css_class="custom-well"
                    ),
                    css_class="span7"
                ),
                Div(
                    Div(
                        BootstrapFieldset(u'Critères optionnels', 'price', 'surface', 'habitation_type', 'nb_of_rooms', 'nb_of_bedrooms', css_id="general", collapse_in='in'),
                        BootstrapFieldset(u'Situation', 'floor', 'ground_floor', 'top_floor', 'not_overlooked', 'duplex', css_id="situation", ),
                        BootstrapFieldset(u'A propos de l\'immeuble', 'elevator', 'intercom', 'digicode', 'doorman', css_id="about", ),
                        BootstrapFieldset(u'Commodités', 'heating', 'kitchen', 'cellar', 'parking', 'swimming_pool', 'alarm', 'air_conditioning', 'fireplace', 'terrace', 'balcony', css_id="com", ),
                        BootstrapFieldset(u'Pièces', 'separate_dining_room', 'separate_toilet', 'bathroom', 'shower', 'separate_entrance',  css_id="rooms", ),
                        BootstrapFieldset(u'Critères énergétiques', 'energy_consumption', 'emission_of_greenhouse_gases', css_id="energy",),
                        css_class="custom-well"
                    ),
                    css_class="span5"
                ),
            css_class="row"
        )
        super(HomeForSaleAdFilterSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeForSaleAd
        logger.debug('class Meta of HomeForSaleAdFilterSetForm')
        fields = ('location', )  # don't know why I need to put this field, but well ... if it's the only bug

    class Media:
        js = ('js/collapse-icon.js',)
