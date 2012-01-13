from django.core.management.base import BaseCommand, CommandError
from sites.achetersanscom.ads.models import HomeForSaleAd
from pygeocoder import Geocoder
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    def handle(self, *args, **options):
        homes = HomeForSaleAd.objects.all()
        for home in homes:
            print home.user_entered_address
            geocode = Geocoder.geocode(home.user_entered_address)
            coordinates = geocode[0].coordinates
            print coordinates
            pnt = Point(coordinates[1], coordinates[0], srid=900913)
            home.location = pnt
            home.save()