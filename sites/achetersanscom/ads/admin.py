from django.contrib import admin
from moderation.admin import ModerationAdmin
from models import HomeForSaleAd

admin.site.register(HomeForSaleAd, ModerationAdmin)