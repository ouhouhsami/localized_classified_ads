#-*- coding: utf-8 -*-
import floppyforms as forms
from django.utils.translation import ugettext as _


class PriceField(forms.Field):
    def to_python(self, value):
        """
        Normalize data to price field
        """
        try:
            val = str(value).replace('.', '').replace(' ', '').replace(',', '')
            return int(val)
        except:
            raise forms.ValidationError(_(u"Entrez un prix en euros."))


class SurfaceField(forms.Field):
    def to_python(self, value):
        """
        Normalize data to surface field
        """
        if not value:
            return None
        try:
            return round(float(str(value).replace(',', '.')))
        except:
            raise forms.ValidationError(_(u"Entrez une surface en mètres carré."))
