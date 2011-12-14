from django.core.management.base import BaseCommand, CommandError
from ads.factory import HomeForSaleAdMockup
from ads.models import HomeForSaleAd

class Command(BaseCommand):

    def handle(self, *args, **options):
        mockup = HomeForSaleAdMockup(HomeForSaleAd)
        entries = mockup.create(2000)        