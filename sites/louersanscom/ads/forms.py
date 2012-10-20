#-*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML
from crispy_forms.bootstrap import AppendedText, Field

from django.utils.translation import ugettext as _
from django import forms

from geoads.widgets import BooleanExtendedNumberInput, BooleanExtendedInput
from utils.bootstrap import MultiField, BootstrapFieldset

from models import HomeForRentAd
from utils.forms import BaseModeratedAdForm


class HomeForRentAdForm(BaseModeratedAdForm):
    # todo add my price and my surface fields

    separate_toilet = forms.CharField(
        label='',
        required=False,
        widget=BooleanExtendedNumberInput(
            attrs={'label': _(u"Toilettes séparés"),
                   'detail': _(u"préciser leur nombre")})
    )

    bathroom = forms.CharField(
        label='',
        required=False,
        widget=BooleanExtendedNumberInput(
            attrs={'label': _(u"Salle de bain"),
                   'detail': _(u"préciser leur nombre")})
    )

    shower = forms.CharField(
        label='',
        required=False,
        widget=BooleanExtendedNumberInput(
            attrs={'label': _(u"Salle d'eau (douche)"),
                   'detail': _(u"préciser leur nombre")})
    )

    furnished = forms.CharField(
        label='',
        required=False,
        widget=BooleanExtendedInput(
            attrs={'label': _(u"Habitation meublée"),
                   'detail': _(u"donner le détail")})
    )

    balcony = forms.CharField(
        label='',
        required=False,
        widget=BooleanExtendedNumberInput(
            attrs={'label': _(u"Balcon"),
                    'detail': _(u"préciser la surface (m²)")})
    )

    terrace = forms.CharField(
        label='',
        required=False,
        widget=BooleanExtendedNumberInput(
             attrs={'label': _(u"Terrasse"),
                    'detail': _(u"préciser la surface (m²)")})
    )

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

    def clean_furnished(self):
        data = self.cleaned_data['furnished']
        if data == '':
            data = None
        return data

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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(u'Informations générales',
                     'habitation_type', AppendedText('price', '€/mois', css_class="input-mini"), 
                     AppendedText('maintenance_charges', '€/mois', css_class="input-mini"),
                     AppendedText('surface', 'm²', css_class="input-mini"), 
                     AppendedText('surface_carrez', 'm²', css_class="input-mini"), 
                     'nb_of_rooms', 'nb_of_bedrooms', 'user_entered_address', 
                     MultiField('', 'colocation', 'furnished', css_class='control-group', label_class='control-label'), 
                     AppendedText('housing_tax', '€/an', css_class="input-mini"),
                     css_class='atom house apartment parking others base'),
            Fieldset(u'Surface du terrain', 
                     AppendedText('ground_surface', 'm²', css_class="input-mini"), 
                     css_class='atom house'),
            Fieldset(u'Situation du logement dans l\'immeuble', 
                      'floor', 
                      MultiField('', 'ground_floor', 'top_floor', 'not_overlooked', 'duplex', css_class='control-group', label_class='control-label'),
                      'orientation', css_class='atom apartment'),
            Fieldset(u'A propos de l\'immeuble', 
                      MultiField('', 'elevator', 'intercom', 'digicode', 'doorman', css_class='control-group', label_class='control-label'), 
                      css_class='atom apartment'),
            Fieldset(u'Commodités', 'heating', 'parking', 
                       MultiField('', 'terrace' ,'balcony', css_class='control-group', label_class='control-label'), 
                       css_class='atom apartment house others'),
            Fieldset(u'Pièces', 
                       MultiField('', 'separate_dining_room', 'separate_toilet', 'bathroom', 'shower', css_class='control-group', label_class='control-label'), 
                       css_class='atom apartment house others'),
            Fieldset(u'Informations complémentaires', 'description',
                       css_class = "atom house apartment parking others", css_id="description"),
            Div(
                Submit('submit', "Enregistrer l'annonce", css_class="btn btn-large btn-block btn-primary", style="width:100%")
            )
        )
        super(HomeForRentAdForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeForRentAd
        exclude = ('user', 'delete_date', 'location', 'address', 'visible')

    class Media:
        js = ('js/edit_form.js',)


class HomeForRentAdFilterSetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'get'
        self.helper.form_action = ''
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
                        BootstrapFieldset(u'Critères optionnels', 'habitation_type', 'price', 'surface', 'nb_of_rooms', 'nb_of_bedrooms',  'colocation', 'furnished', 'elevator', css_id="general", collapse_in='in'),
                        css_class="custom-well"
                        ),
                    css_class="span5"
                    ),
            css_class="row"
        )
        super(HomeForRentAdFilterSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeForRentAd
        fields = ('location', )  # don't know why I need to put this field, but well ... if it's the only bug

    class Media:
        js = ('js/collapse-icon.js',)
