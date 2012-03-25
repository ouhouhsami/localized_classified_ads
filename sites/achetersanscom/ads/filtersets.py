# coding=utf-8
import django_filters
from django.forms import widgets

from ads.filters import LocationFilter, BooleanForNumberFilter
from ads.widgets import GooglePolygonWidget, IndifferentNullBooleanSelect, SpecificRangeWidget

from models import HomeForSaleAd, HABITATION_TYPE_CHOICES
from forms import HomeForSaleAdFilterSetForm

class NicerFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(NicerFilterSet, self).__init__(*args, **kwargs)        
        for name, field in self.filters.iteritems():
            if isinstance(field, django_filters.filters.BooleanFilter):
                field.widget = IndifferentNullBooleanSelect()
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Tous types"), ] + list(field.extra['choices']))

class HomeForSaleAdFilterSet(NicerFilterSet):
    price = django_filters.OpenRangeNumericFilter(label="Budget (€)", 
                                       widget=SpecificRangeWidget({'size':'6'}))
    surface = django_filters.OpenRangeNumericFilter(label="Surface (m²)", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    nb_of_rooms = django_filters.OpenRangeNumericFilter(label="Nb. de pièces", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    nb_of_bedrooms = django_filters.OpenRangeNumericFilter(label="Nb. de chambres", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    ground_surface = django_filters.OpenRangeNumericFilter(label="(m²)", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    floor = django_filters.OpenRangeNumericFilter(label="Etage", 
                                         widget=SpecificRangeWidget({'size':'6'}))
    habitation_type = django_filters.MultipleChoiceFilter(label="Type d'habitation", 
                                         widget = widgets.CheckboxSelectMultiple(),
                                         choices = HABITATION_TYPE_CHOICES)
    location = LocationFilter(widget=GooglePolygonWidget(), 
                              label="Localisation", help_text="Localisation", required=False)
    balcony = BooleanForNumberFilter(label="Balcon", widget = IndifferentNullBooleanSelect())
    terrace = BooleanForNumberFilter(label="Terrasse", widget = IndifferentNullBooleanSelect())
    separate_toilet = BooleanForNumberFilter(label="Toilettes séparés", widget = IndifferentNullBooleanSelect())
    bathroom = BooleanForNumberFilter(label="Salle de bain", widget = IndifferentNullBooleanSelect())
    shower = BooleanForNumberFilter(label="Salle d'eau (douche)", widget = IndifferentNullBooleanSelect())
    def __init__(self, *args, **kwargs):
        # improve : set default to none if key doesnt exist
        try:
            search = kwargs['search']
            del kwargs['search']
        except:
            search = None
        super(HomeForSaleAdFilterSet, self).__init__(*args, **kwargs)
        if search:
            self.form.fields['location'].widget = GooglePolygonWidget(ads=self.qs, search=search, fillColor="#FFB82E", strokeColor="#20B2AA")
        else:
            self.form.fields['location'].widget = GooglePolygonWidget(ads=[], search=search, fillColor="#FFB82E", strokeColor="#20B2AA")
    class Meta:
        model = HomeForSaleAd
        form = HomeForSaleAdFilterSetForm
        fields = ['price', 'surface', 'habitation_type', 
                  'location', 'nb_of_rooms', 'nb_of_bedrooms', 
                  'energy_consumption', 'emission_of_greenhouse_gases', 
                  'ground_surface', 'floor', 'top_floor', 'not_overlooked', 'ground_floor',
                  'elevator', 'intercom', 'digicode', 'doorman', 
                  'elevator', 'heating', 'kitchen', 'duplex', 
                  'swimming_pool', 'alarm', 'air_conditioning', 
                  'fireplace', 'terrace', 'balcony', 
                  'separate_dining_room', 'separate_toilet', 
                  'bathroom', 'shower', 'separate_entrance', 'cellar', 
                  'parking']