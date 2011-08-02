# coding=utf-8
import django_filters
from django_filters.filters import Filter
from django_filters.widgets import RangeWidget
from django import forms
from django.forms import widgets
from filters import LocationFilter
from widgets import PolygonWidget, IndifferentNullBooleanSelect
from models import HomeForSaleAd, HomeForRentAd, HABITATION_TYPE_CHOICES, PARKING_CHOICES
from forms import HomeForSaleAdFilterSetForm, HomeForRentAdFilterSetForm
from django.utils.translation import ugettext

class SpecificRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.TextInput(attrs={'placeholder':'min'}), forms.TextInput(attrs={'placeholder':'max'}))
        super(SpecificRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u'-'.join(rendered_widgets)


indifferent_choices = ((u'1', ugettext('Indifferent')),(u'2', ugettext('Yes')),(u'3', ugettext('No')))

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
            #print field
            if isinstance(field, django_filters.filters.BooleanFilter):
                field.widget = IndifferentNullBooleanSelect()
                #field.extra['choices'] = indifferent_choices 
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Tous types"), ] + list(field.extra['choices']))
                #pass
        

class HomeAdFilterSet(NicerFilterSet):
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
    location = LocationFilter(widget=PolygonWidget(ads=[]), label="Localisation", help_text="Localisation", required=False)

    #parking = django_filters.MultipleChoiceFilter(label="Parking", 
    #                                     widget = widgets.CheckboxSelectMultiple(),
    #                                     choices = PARKING_CHOICES)

    class Meta:
        #model = HomeForSaleAd
        #form = HomeForSaleAdFilterSetForm
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
                  'parking', 'orientation']

class HomeForSaleAdFilterSet(HomeAdFilterSet):
    price = django_filters.OpenRangeNumericFilter(label="Budget (€)", 
                                       widget=SpecificRangeWidget({'size':'6'}))

    def __init__(self, *args, **kwargs):
        search = kwargs['search']
        del kwargs['search']
        super(HomeForSaleAdFilterSet, self).__init__(*args, **kwargs)
        if search:
            self.form.fields['location'].widget = PolygonWidget(ads=self.qs, search=search)
        else:
            self.form.fields['location'].widget = PolygonWidget(ads=[], search=search)
        #print self.form.fields['location']

    class Meta:
        model = HomeForSaleAd
        form = HomeForSaleAdFilterSetForm

class HomeForRentAdFilterSet(HomeAdFilterSet):
    price = django_filters.OpenRangeNumericFilter(label="Loyer (€) / mois", 
                                       widget=SpecificRangeWidget({'size':'6'}))

    def __init__(self, *args, **kwargs):
        search = kwargs['search']
        del kwargs['search']
        super(HomeForRentAdFilterSet, self).__init__(*args, **kwargs)
        if search:
            self.form.fields['location'].widget = PolygonWidget(ads=self.qs, search=search)
        else:
            self.form.fields['location'].widget = PolygonWidget(ads=[], search=search)
        #print self.form.fields['location']

    class Meta:
        model = HomeForRentAd
        form = HomeForRentAdFilterSetForm
        fields = ['price', 'surface', 'habitation_type', 'colocation', 'furnished', 
                  'location', 'nb_of_rooms', 'nb_of_bedrooms', 
                  'energy_consumption', 'emission_of_greenhouse_gases', 
                  #'ground_surface', 
                  'floor', 'top_floor', 'not_overlooked', 'ground_floor',
                  'elevator', 'intercom', 'digicode', 'doorman', 
                  'elevator', 'heating', 'kitchen', 'duplex', 
                  'swimming_pool', 'alarm', 'air_conditioning', 
                  'fireplace', 'terrace', 'balcony', 
                  'separate_dining_room', 'separate_toilet', 
                  'bathroom', 'shower', 'separate_entrance', 'cellar', 
                  'parking', 'orientation']