# coding=utf-8
from itertools import chain

from django.utils.encoding import force_unicode
from models import *
import floppyforms
from django.template import loader
from floppyforms.gis.widgets import BaseGeometryWidget
from floppyforms.widgets import Input, NumberInput
from django.utils.translation import ugettext


class Select(floppyforms.Select, Input):
    template_name = 'floppyforms/select.html'

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        #just because of the line below, we need to not CHAIN
        #choices = chain(self.choices, choices)
        final_choices = []
        for option_value, option_label in choices:
            final_choices.append((force_unicode(option_value), option_label))
        extra = {'choices': final_choices}
        return Input.render(self, name, value, attrs=attrs,
                            extra_context=extra)


class IndifferentNullBooleanSelect(floppyforms.NullBooleanSelect, Select):

    def render(self, name, value, attrs=None, choices=()):
        choices = ((u'1', ugettext(u'Indifférent')),
                   (u'2', ugettext('Yes')),
                   (u'3', ugettext('No')))
        try:
            value = {True: u'2', False: u'3', u'2': u'2', u'3': u'3'}[value]
        except KeyError:
            value = u'1'
        return Select.render(self, name, value, attrs, choices=choices)

class BaseGMapWidget(BaseGeometryWidget):
    """A Google Maps base widget"""
    map_srid = 900913
    template_name = 'floppyforms/gis/google.html'

    class Media:
        js = (
            'js/OpenLayers.js',
            'floppyforms/js/MapWidget.js',
            'js/map.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )
        css = {
            'all': ('css/map.css',)
        }


class BaseSimpleGMapWidget(BaseGeometryWidget):
    map_srid = 900913
    template_name = 'floppyforms/gis/simple_google.html'
    class Media:
        js = (
            'js/OpenLayers.js',
            'floppyforms/js/MapWidget.js',
            'js/map.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )
        css = {
            'all': ('css/map.css',)
        }
    

class PolygonWidget(floppyforms.gis.PolygonWidget, BaseGMapWidget):
    map_width = '645'
    is_polygon = True
    geom_type = 'POLYGON'
    map_srid = 900913
    display_wkt = True
    
    def __init__(self, *args, **kwargs):
        self.ads = kwargs.get('ads', None)
        self.controls = kwargs.get('controls', True)
        self.search = kwargs.get('search', False)
        super(PolygonWidget, self).__init__()

    def get_context_data(self):
        ctx = super(PolygonWidget, self).get_context_data()
        ctx['ads'] = self.ads
        ctx['search'] = self.search
        return ctx

    class Media:
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
            '/static/js/CustomZoomPanel.js',
            '/static/js/MapWidgetOverride.js',
        )


'''
class GMapPointWidget(floppyforms.gis.PointWidget, BaseGMapWidget):
    pass
'''

class GMapPointWidget(floppyforms.gis.PointWidget, BaseSimpleGMapWidget):
    pass


class CustomPointWidget(GMapPointWidget):
    map_width = 645
    map_height = 400
    map_srid = 900913
    #display_wkt = True

    def __init__(self, *args, **kwargs): 
        self.ads = kwargs.get('ads', None)
        if 'id' in kwargs:
            self.id = 'location'
        self.controls = kwargs.get('controls', True)
        super(CustomPointWidget, self).__init__()

    def get_context_data(self):
        ctx = super(CustomPointWidget, self).get_context_data()
        ctx['ads'] = self.ads
        ctx['controls'] = self.controls
        if hasattr(self, 'id'):
            self.attrs['id'] = self.id           
        return ctx

class GooglePolygonWidget(Input):
    template_name = 'floppyforms/gis/poly_google.html'
    def __init__(self, *args, **kwargs):
        self.ads = kwargs.get('ads', None)
        self.search = kwargs.get('search', False)
        super(GooglePolygonWidget, self).__init__()
    def get_context_data(self):
        ctx = super(GooglePolygonWidget, self).get_context_data()
        ctx['ads'] = self.ads
        ctx['search'] = self.search
        return ctx
    class Media:
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
            'js/proj4js-combined.js',
            'js/poly_googlemap.js',
        )

class GooglePointWidget(Input):
    template_name = 'floppyforms/gis/point_google.html'
    class Media:
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
            'js/proj4js-combined.js',
            'js/point_googlemap.js',
        )

class BooleanExtendedNumberInput(NumberInput):
    template_name = 'floppyforms/boolean_extended_number_input.html'
    # we should add jquery, but it's on all site pages so ...
