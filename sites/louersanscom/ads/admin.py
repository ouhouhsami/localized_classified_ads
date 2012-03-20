from django.contrib import admin
from moderation.admin import ModerationAdmin
from models import HomeForRentAd

admin.site.register(HomeForRentAd, ModerationAdmin)