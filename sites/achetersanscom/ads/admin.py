from django.contrib import admin

from ads.admin import AdAdmin

from models import HomeForSaleAd

admin.site.register(HomeForSaleAd, AdAdmin)