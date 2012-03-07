# coding=utf-8
"""
Ads app admin module
"""

from django.contrib import admin
from moderation.admin import ModerationAdmin
from ads.models import AdSearch, AdContact, AdPicture


class AdAdmin(ModerationAdmin):
    """
    Base moderation admin for ad model
    """
    pass

admin.site.register(AdSearch)
admin.site.register(AdContact)
admin.site.register(AdPicture)
