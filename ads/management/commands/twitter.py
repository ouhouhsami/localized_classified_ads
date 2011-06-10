# coding=utf-8
import oauth2 as oauth
import urlparse
import cgi

from django.core.management.base import BaseCommand, CommandError
from ads.models import *
from django.conf import settings
from django.template.defaultfilters import urlencode
from django.contrib.gis.geos import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        token = oauth.Token(key=settings.TWITTER_ACCESS_TOKEN_KEY, 
                            secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
        consumer = oauth.Consumer(settings.TWITTER_CONSUMER_KEY, 
                                  settings.TWITTER_CONSUMER_SECRET)
        client = oauth.Client(consumer, token)

        for ad in HomeForSaleAd.objects.all():
            habitation_type = ad.get_habitation_type_display()
            price = ad.price
            surface = int(ad.surface)
            rooms = int(ad.nb_of_rooms)
            status = u'#achetersanscom %s - %s€ - %sm² - %s pièces' % (habitation_type, 
                                                    price, surface, rooms)
            pnt = GEOSGeometry('SRID=%s;%s' % (ad.location.srid, ad.location.wkt))
            pnt.transform(4326)
            latitude = pnt.y
            longitude = pnt.x
            params = 'status=%s&lat=%s&long=%s&display_coordinates=true' % (urlencode(status), latitude, longitude)
            resp, content = client.request(
                'http://api.twitter.com/1/statuses/update.xml?%s' % (params),
                "POST"
            )
            
        