from django.contrib import admin
from models import AdSearch, AdContact, AdPicture
import floppyforms
from django.forms import ModelForm
from moderation.admin import ModerationAdmin
from widgets import CustomPointWidget, GooglePointWidget

class AdAdmin(ModerationAdmin):
    pass

admin.site.register(AdSearch)
admin.site.register(AdContact)
admin.site.register(AdPicture)
