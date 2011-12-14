from django.contrib import admin
from models import *
import floppyforms
from django.forms import ModelForm
from moderation.admin import ModerationAdmin
from widgets import CustomPointWidget, GooglePointWidget

class PointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    pass


class UserProfileAdminForm(ModelForm):
    location = floppyforms.gis.PointField(widget = PointWidget)
    class Meta:
        model = UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm


class AdAdmin(ModerationAdmin):
    pass


admin.site.register(HomeForSaleAd, AdAdmin)
admin.site.register(HomeForRentAd, AdAdmin)
admin.site.register(AdSearch)
admin.site.register(AdContact)
