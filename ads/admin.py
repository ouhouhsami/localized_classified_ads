from django.contrib import admin
from models import *
import floppyforms
from django.forms import ModelForm
from moderation.admin import ModerationAdmin

class PointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    pass


class UserProfileAdminForm(ModelForm):
    location = floppyforms.gis.PointField(widget = PointWidget)
    class Meta:
        model = UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm

class HomeForSaleAdAdmin(ModerationAdmin):
    ''' TODO: verify is save_model is overidden w/ geo widgets
    def save_model(self, request, obj, form, change):
        from moderation.helpers import automoderate
        automoderate(obj, request.user)
    '''
    pass


#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HomeForSaleAd, HomeForSaleAdAdmin)
admin.site.register(AdSearch)
admin.site.register(AdContact)
