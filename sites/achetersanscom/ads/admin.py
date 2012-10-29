from django.contrib import admin
from moderation.admin import ModerationAdmin
from models import HomeForSaleAd


class HomeForSaleAdAdmin(ModerationAdmin):
    list_display = ('get_unicode', 'get_owner_email', )

    def get_owner_email(self, obj):
        return '%s' % (obj.user.email)

    get_owner_email.short_description = 'Owner email'

    def get_unicode(self, obj):
        return obj.__unicode__()

admin.site.register(HomeForSaleAd, HomeForSaleAdAdmin)
