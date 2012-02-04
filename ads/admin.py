from django.contrib import admin
from models import AdSearch, AdContact, AdPicture
from moderation.admin import ModerationAdmin

class AdAdmin(ModerationAdmin):
    pass

admin.site.register(AdSearch)
admin.site.register(AdContact)
admin.site.register(AdPicture)
