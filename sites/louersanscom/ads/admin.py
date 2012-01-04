from django.contrib import admin
from ads.admin import AdAdmin
from models import HomeForRentAd

admin.site.register(HomeForRentAd, AdAdmin)