# coding=utf-8
import django_filters
from django_filters.filters import Filter
from django_filters.widgets import RangeWidget
from filters import LocationFilter
from widgets import PolygonWidget
from models import HomeForSaleAd, HABITATION_TYPE_CHOICES
from forms import HomeForSaleAdFilterSetForm

class NicerFilterSet(django_filters.FilterSet):
    # add location field filter
    '''
    filter_overrides = {
        models.LocationField: {
            #'filter_class': django_filters.CharFilter,
            'filter_class': LocationFilter
        }
    }
    '''
    def __init__(self, *args, **kwargs):
        super(NicerFilterSet, self).__init__(*args, **kwargs)
        
        for name, field in self.filters.iteritems():
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Tous types"), ] + list(field.extra['choices']))
                #pass
        


class HomeForSaleAdFilterSet(NicerFilterSet):
    price = django_filters.RangeFilter(label="Budget", 
                                       help_text="min.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max. (€)",
                                       widget=RangeWidget({'size':'6'}))
    surface = django_filters.RangeFilter(label="Surface", 
                                         help_text="min.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max. (m<sup>2</sup>)",
                                         widget=RangeWidget({'size':'6'}))
    nb_of_rooms = django_filters.RangeFilter(label="Nb. de pièces", 
                                         help_text="min.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max.",
                                         widget=RangeWidget({'size':'6'}))
    nb_of_bedrooms = django_filters.RangeFilter(label="Nb. de chambres", 
                                         help_text="min.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max.",
                                         widget=RangeWidget({'size':'6'}))
    ground_surface = django_filters.RangeFilter(label="Surface du terrain", 
                                         help_text="min.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max.",
                                         widget=RangeWidget({'size':'6'}))
    floor = django_filters.RangeFilter(label="Etage", 
                                         help_text="min.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max.",
                                         widget=RangeWidget({'size':'6'}))
    habitation_type = django_filters.MultipleChoiceFilter(label="Type d'habitation", help_text="choix multiple : ctrl+click", choices = HABITATION_TYPE_CHOICES)
    location = LocationFilter(widget=PolygonWidget(ads=[]), label="Localisation", help_text="Localisation", required=False)

    def __init__(self, *args, **kwargs):
        super(HomeForSaleAdFilterSet, self).__init__(*args, **kwargs)
        self.form.fields['location'].widget = PolygonWidget(ads=self.qs)

    class Meta:
        model = HomeForSaleAd
        form = HomeForSaleAdFilterSetForm
        fields = ['price', 'surface', 'habitation_type', 
                  'location', 'nb_of_rooms', 'nb_of_bedrooms', 
                  'energy_consumption', 'emission_of_greenhouse_gases', 
                  'ground_surface', 'floor', 'top_floor',
                  'elevator', 'intercom', 'digicode', 'doorman', 
                  'elevator', 'heating', 'kitchen', 'duplex', 
                  'swimming_pool', 'alarm', 'air_conditioning', 
                  'fireplace', 'parquet', 'terrace', 'balcony', 
                  'separate_dining_room', 'living_room', 'separate_toilet', 
                  'bathroom', 'shower', 'separate_entrance', 'cellar', 
                  'cupboards', 'open_parking', 'box', 'orientation']
