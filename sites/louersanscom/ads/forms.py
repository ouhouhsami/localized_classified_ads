# coding=utf-8

from form_utils.forms import BetterModelForm
from moderation.forms import BaseModeratedObjectForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Div
from crispy_forms.bootstrap import FormActions, AppendedText, PrependedText

from django.utils.translation import ugettext as _
from django import forms


from geoads.widgets import BooleanExtendedNumberInput, BooleanExtendedInput
from geoads.forms import BaseAdForm
from utils.bootstrap import AppendedPrependedText, MultiField

from models import HomeForRentAd

class HomeForRentAdForm(BaseAdForm):
    # todo add my price and my surface fields
    
    separate_toilet = forms.CharField(
        label='', 
        required=False, 
        widget=BooleanExtendedNumberInput(
            attrs={'label':_(u"Toilettes séparés"), 
                   'detail':_(u"préciser leur nombre")})
    )

    bathroom = forms.CharField(
        label='', 
        required=False, 
        widget=BooleanExtendedNumberInput(
            attrs={'label':_(u"Salle de bain"), 
                   'detail':_(u"préciser leur nombre")})
    )

    shower = forms.CharField(
        label='', 
        required=False, 
        widget=BooleanExtendedNumberInput(
            attrs={'label':_(u"Salle d'eau (douche)"), 
                   'detail':_(u"préciser leur nombre")})
    )

    furnished = forms.CharField(
        label='', 
        required=False, 
        widget=BooleanExtendedInput(
            attrs={'label':_(u"Habitation meublée"), 
                   'detail':_(u"donner le détail")})
    )
    
    balcony = forms.CharField(
        label='', 
        required=False, 
        widget=BooleanExtendedNumberInput(
            attrs={'label':_(u"Balcon"), 
                    'detail':_(u"préciser la surface (m²)")})
    )
    
    terrace = forms.CharField(
        label='', 
        required=False, 
        widget=BooleanExtendedNumberInput(
             attrs={'label':_(u"Terrasse"), 
                    'detail':_(u"préciser la surface (m²)")})
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
        )
        super(HomeForRentAdForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeForRentAd
        exclude = ('user', 'delete_date', 'location', 'address', 'visible')
        #fieldsets = [('title', {'fields': ['habitation_type', 'price', 'maintenance_charges','surface', 'surface_carrez', 'nb_of_rooms', 'nb_of_bedrooms', 'user_entered_address', 'colocation', 'furnished', 'housing_tax'], 'legend': 'Informations générales', 'classes':['house', 'apartment', 'parking', 'others', 'base']}),
        #             ('ground_surface', {'fields' :['ground_surface'], 'legend': 'Surface du terrain', 'classes':['house']}),
        #             ('about_floor', {'fields' :['floor', 'ground_floor', 'top_floor', 'not_overlooked', 'duplex', 'orientation'], 'legend': 'Situation du logement dans l\'immeuble', 'classes': ['apartment']}),
        #             ('about_flat', {'fields' :['elevator', 'intercom', 'digicode', 'doorman'], 'legend': 'A propos de l\'immeuble', 'classes': ['apartment']}),
        #             ('conveniences', {'fields' :['heating', 'parking', 'terrace' ,'balcony'], 'legend': 'Commodités', 'classes': ['apartment', 'house', 'others']}),
        #             ('rooms', {'fields' :['separate_dining_room', 'separate_toilet', 'bathroom', 'shower'], 'legend': 'Pièces',  'classes': ['apartment', 'house', 'others']}),
        #             ('description', {'fields': ['description'], 'legend':'Description complémentaire', 'classes':['house', 'apartment', 'parking', 'others']})
        #            ]

class HomeForRentAdFilterSetForm(BetterModelForm):

    def clean_price(self):
        pass

    def clean_surface(self):
        pass

    def clean_nb_of_rooms(self):
        pass

    def nb_of_bedrooms(self):
        pass

    def clean_habitation_type(self):
        pass

    def clean_location(self):
        pass

    def clean_colocation(self):
        pass

    def clean_furnished(self):
        pass

    def clean_elevator(self):
        pass

    class Meta:
        model = HomeForRentAd   
        fieldsets = [('location', {'fields': ['location'], 'legend': 'Dessiner votre zone de recherche en cliquant sur la carte'}),
                     ('general_information', {'fields' : ['habitation_type', 'price', 'surface', 'nb_of_rooms', 'nb_of_bedrooms',  'colocation', 'furnished', 'elevator']}),
                     ]       

