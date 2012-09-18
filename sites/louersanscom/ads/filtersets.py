# coding=utf-8
import django_filters

from geoads.widgets import GooglePolygonWidget, IndifferentNullBooleanSelect, SpecificRangeWidget
from geoads.filters import LocationFilter, BooleanForNumberFilter

from models import HomeForRentAd
from forms import HomeForRentAdFilterSetForm

from utils.widgets import BootstrapSpecificRangeWidget
from geoads.filtersets import AdFilterSet


class NicerFilterSet(AdFilterSet):
    def __init__(self, *args, **kwargs):
        super(NicerFilterSet, self).__init__(*args, **kwargs)
        for name, field in self.filters.iteritems():
            if isinstance(field, django_filters.filters.BooleanFilter):
                field.widget = IndifferentNullBooleanSelect()
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Tous types"), ] + list(field.extra['choices']))


class HomeForRentAdFilterSet(NicerFilterSet):
    price = django_filters.OpenRangeNumericFilter(label="Loyer",
                                       widget=BootstrapSpecificRangeWidget({'size': '6'}, '€/mois'))
    nb_of_rooms = django_filters.OpenRangeNumericFilter(label="Nb. de pièces",
                                         widget=SpecificRangeWidget({'size': '6'}))
    nb_of_bedrooms = django_filters.OpenRangeNumericFilter(label="Nb. de chambres",
                                         widget=SpecificRangeWidget({'size': '6'}))
    surface = django_filters.OpenRangeNumericFilter(label="Surface",
                                       widget=BootstrapSpecificRangeWidget({'size': '6'}, 'm²'))
    furnished = BooleanForNumberFilter(label="Habitation meublée", widget=IndifferentNullBooleanSelect())
    location = LocationFilter(widget=GooglePolygonWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super(HomeForRentAdFilterSet, self).__init__(*args, **kwargs)
        #if self.search:
        #    self.form.fields['location'].widget = GooglePolygonWidget(ads=self.qs, search=self.search, fillColor="pink", strokeColor="#9d81a1")
        #else:
        #    self.form.fields['location'].widget = GooglePolygonWidget(ads=[], search=self.search, fillColor="pink", strokeColor="#9d81a1")
        self.form.fields['location'].widget = GooglePolygonWidget(ads=[], fillColor="pink", strokeColor="#9d81a1")

    class Meta:
        model = HomeForRentAd
        form = HomeForRentAdFilterSetForm
        #fields = ['habitation_type', 'price', 'surface', 'nb_of_rooms', 'nb_of_bedrooms',  'colocation', 'furnished', 'elevator', 'location']
