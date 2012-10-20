#-*- coding: utf-8 -*-
import logging
import django_filters
from django.forms import widgets

from geoads.filters import LocationFilter, BooleanForNumberFilter
from geoads.widgets import (LeafletWidget,
    IndifferentNullBooleanSelect, SpecificRangeWidget)
from geoads.templatetags.ads_tag import has_value

from utils.bootstrap import BootstrapFieldset

from models import HomeForSaleAd, HABITATION_TYPE_CHOICES
from forms import HomeForSaleAdFilterSetForm

from utils.widgets import BootstrapSpecificRangeWidget
from utils.filtersets import NicerFilterSet

logger = logging.getLogger(__name__)


class HomeForSaleAdFilterSet(NicerFilterSet):
    """
    FilterSet for HomeForSaleAd
    Used to filter home for sale ads in the home page

    """
    price = django_filters.OpenRangeNumericFilter(label="Budget",
        widget=BootstrapSpecificRangeWidget({'size': '6'}, '€'))
    surface = django_filters.OpenRangeNumericFilter(label="Surface",
        widget=BootstrapSpecificRangeWidget({'size': '6'}, 'm²'))
    nb_of_rooms = django_filters.OpenRangeNumericFilter(label="Nb. de pièces",
        widget=SpecificRangeWidget({'size': '6'}))
    nb_of_bedrooms = django_filters.OpenRangeNumericFilter(label="Nb. de chambres",
        widget=SpecificRangeWidget({'size': '6'}))
    floor = django_filters.OpenRangeNumericFilter(label="Etage",
        widget=SpecificRangeWidget({'size': '6'}))
    habitation_type = django_filters.MultipleChoiceFilter(label="Type d'habitation",
        widget=widgets.CheckboxSelectMultiple(), choices=HABITATION_TYPE_CHOICES)
    location = LocationFilter(widget=LeafletWidget(),
        label="Localisation", required=False)
    balcony = BooleanForNumberFilter(label="Balcon",
        widget=IndifferentNullBooleanSelect())
    terrace = BooleanForNumberFilter(label="Terrasse",
        widget=IndifferentNullBooleanSelect())
    separate_toilet = BooleanForNumberFilter(label="Toilettes séparés",
        widget=IndifferentNullBooleanSelect())
    bathroom = BooleanForNumberFilter(label="Salle de bain",
        widget=IndifferentNullBooleanSelect())
    shower = BooleanForNumberFilter(label="Salle d'eau (douche)",
        widget=IndifferentNullBooleanSelect())

    def __init__(self, *args, **kwargs):
        super(HomeForSaleAdFilterSet, self).__init__(*args, **kwargs)
        self.form.fields['location'].widget = LeafletWidget(ads=self.qs, fillColor="#FFB82E", strokeColor="#20B2AA")
        # here we open collapsible search filter item
        for f in self.form.helper.layout.fields[1].fields[0].fields:
            for field in f.fields:
                if not isinstance(self.form.fields[field], BootstrapFieldset) and has_value(self.form[field]) == 'has_value':
                    f.set_collapse('in')

    class Meta:
        model = HomeForSaleAd
        form = HomeForSaleAdFilterSetForm
        # here we exclude for crispy-form render fields off
        logger.debug('class Meta of HomeForSaleAdFilterSet')
        exclude = ('user', 'delete_date', 'address', 'visible',
           'user_entered_address', 'description', 'ground_surface',
           'orientation', 'housing_tax', 'surface_carrez',
           'maintenance_charges', 'ad_valorem_tax', 'slug',
           'update_date', 'create_date')
