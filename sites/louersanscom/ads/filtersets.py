# coding=utf-8
import django_filters

from ads.filtersets import SpecificRangeWidget
from ads.widgets import GooglePolygonWidget, IndifferentNullBooleanSelect
from ads.filters import LocationFilter, BooleanForNumberFilter

from models import HomeForRentAd
from forms import HomeForRentAdFilterSetForm


class NicerFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(NicerFilterSet, self).__init__(*args, **kwargs)        
        for name, field in self.filters.iteritems():
            if isinstance(field, django_filters.filters.BooleanFilter):
                field.widget = IndifferentNullBooleanSelect()
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Tous types"), ] + list(field.extra['choices']))

class HomeForRentAdFilterSet(NicerFilterSet):
    price = django_filters.OpenRangeNumericFilter(label="Loyer (€/mois)", 
                                       widget=SpecificRangeWidget({'size':'6'}))
    nb_of_rooms = django_filters.OpenRangeNumericFilter(label="Nb. de pièces", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    nb_of_bedrooms = django_filters.OpenRangeNumericFilter(label="Nb. de chambres", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    surface = django_filters.OpenRangeNumericFilter(label="Surface (m²)", 
                                       widget=SpecificRangeWidget({'size':'6'}))
    furnished = BooleanForNumberFilter(label="Habitation meublée", widget = IndifferentNullBooleanSelect())
    location = LocationFilter(widget=GooglePolygonWidget(), 
                              label="Localisation", help_text="Localisation", required=False)
    def __init__(self, *args, **kwargs):
        search = kwargs['search']
        del kwargs['search']
        super(HomeForRentAdFilterSet, self).__init__(*args, **kwargs)
        if search:
            self.form.fields['location'].widget = GooglePolygonWidget(ads=self.qs, search=search, fillColor="pink", strokeColor="#9d81a1")
        else:
            self.form.fields['location'].widget = GooglePolygonWidget(ads=[], search=search, fillColor="pink", strokeColor="#9d81a1")

    class Meta:
        model = HomeForRentAd
        form = HomeForRentAdFilterSetForm
        fields = ['habitation_type', 'price', 'surface', 'nb_of_rooms', 'nb_of_bedrooms',  'colocation', 'furnished', 'elevator', 'location']
