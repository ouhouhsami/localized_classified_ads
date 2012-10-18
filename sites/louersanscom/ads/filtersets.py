# coding=utf-8
import django_filters

from geoads.widgets import LeafletWidget, IndifferentNullBooleanSelect, SpecificRangeWidget
from geoads.filters import LocationFilter, BooleanForNumberFilter

from models import HomeForRentAd
from forms import HomeForRentAdFilterSetForm

from utils.widgets import BootstrapSpecificRangeWidget
from utils.filtersets import NicerFilterSet


class HomeForRentAdFilterSet(NicerFilterSet):
    """
    FilterSet for HomeForRentAd
    Used to filter home for rent ads in the home page

    """
    price = django_filters.OpenRangeNumericFilter(label="Loyer",
        widget=BootstrapSpecificRangeWidget({'size': '6'}, '€/mois'))
    nb_of_rooms = django_filters.OpenRangeNumericFilter(label="Nb. de pièces",
        widget=SpecificRangeWidget({'size': '6'}))
    nb_of_bedrooms = django_filters.OpenRangeNumericFilter(label="Nb. de chambres",
        widget=SpecificRangeWidget({'size': '6'}))
    surface = django_filters.OpenRangeNumericFilter(label="Surface",
        widget=BootstrapSpecificRangeWidget({'size': '6'}, 'm²'))
    furnished = BooleanForNumberFilter(label="Habitation meublée",
        widget=IndifferentNullBooleanSelect())
    location = LocationFilter(widget=LeafletWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super(HomeForRentAdFilterSet, self).__init__(*args, **kwargs)
        self.form.fields['location'].widget = LeafletWidget(ads=[], fillColor="pink", strokeColor="#9d81a1")

    class Meta:
        model = HomeForRentAd
        form = HomeForRentAdFilterSetForm
        # here we filter for crispy-form render fields off
        fields = ['habitation_type', 'price', 'surface', 'nb_of_rooms', 'nb_of_bedrooms',  'colocation', 'furnished', 'elevator', 'location']
