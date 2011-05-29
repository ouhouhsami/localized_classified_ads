from models import *
import floppyforms
from django.template import loader

class PolygonWidget(floppyforms.gis.PolygonWidget, floppyforms.gis.BaseGMapWidget):
    map_width = '610'
    is_polygon = True
    geom_type = 'POLYGON'
    map_srid = 900913
    
    def __init__(self, *args, **kwargs):
        self.ads = kwargs.get('ads', None)
        self.controls = kwargs.get('controls', True)
        super(PolygonWidget, self).__init__()

    def get_context_data(self):
        ctx = super(PolygonWidget, self).get_context_data()
        ctx['ads'] = self.ads
        return ctx

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )

class GMapPointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    pass

class CustomPointWidget(GMapPointWidget):
    map_width = 894
    map_height = 400
    map_srid = 900913
    display_wkt = True

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