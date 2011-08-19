from django_filters.filters import Filter
import floppyforms 
from django.contrib.gis.geos import fromstr
#from django.contrib.gis.db import models

class LocationFilter(Filter):
    field_class = floppyforms.gis.PolygonField

    def __init__(self, *args, **kwargs):
        super(LocationFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        # very very bad hack because of default manager in HomeForSaleAd
        # try / except is here because of email alert command (don't know why)
        try:
            qs = qs.filter(_relation_object__moderation_status = 1)
        except:
            qs = qs
        lookup = 'within'
        if not value:
            return qs
        if value:
            value = fromstr(value)
            return qs.filter(**{'%s__%s' % (self.name, lookup): value})

class BooleanForNumberFilter(Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        else:
            return qs.filter(**{'%s__isnull' % (self.name): not(value)})